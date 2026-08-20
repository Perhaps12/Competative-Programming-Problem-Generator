import * as cdk from "aws-cdk-lib";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import { Construct } from "constructs";

interface LeetcodeCloneStackProps extends cdk.StackProps {
  /** Name of an EXISTING EC2 key pair (created manually in the AWS console/CLI beforehand). */
  keyPairName: string;
  /** HTTPS clone URL of your GitHub repo, e.g. https://github.com/you/repo.git */
  githubRepoUrl: string;
}

export class LeetcodeCloneStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: LeetcodeCloneStackProps) {
    super(scope, id, props);

    if (!props.keyPairName) {
      throw new Error(
        "Missing required context: keyPairName. Pass with -c keyPairName=your-key-name"
      );
    }
    if (!props.githubRepoUrl) {
      throw new Error(
        "Missing required context: githubRepoUrl. Pass with -c githubRepoUrl=https://github.com/you/repo.git"
      );
    }

    // Use the account's default VPC rather than creating a new one --
    // avoids the extra cost/complexity of a custom VPC (e.g. NAT gateways)
    // for a single-instance deployment like this.
    const vpc = ec2.Vpc.fromLookup(this, "DefaultVpc", { isDefault: true });

    // Security group: SSH, HTTP, HTTPS open to the internet. Postgres and
    // Piston are NOT exposed here -- they're only reachable inside the
    // Docker network, same as the manual setup.
    const securityGroup = new ec2.SecurityGroup(this, "AppSecurityGroup", {
      vpc,
      description: "Leetcode Clone - SSH, HTTP, HTTPS",
      allowAllOutbound: true,
    });
    securityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(22), "SSH");
    securityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80), "HTTP");
    securityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(443), "HTTPS");

    // Ubuntu 24.04 LTS, x86_64 -- matches what we confirmed works with
    // Piston (arm64/Graviton hit an "exec format error" -- see project notes).
    const machineImage = ec2.MachineImage.fromSsmParameter(
      "/aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id",
      { os: ec2.OperatingSystemType.LINUX }
    );

    // Startup script: installs Docker and clones the repo automatically.
    // Deliberately does NOT create .env or run `docker compose up` -- those
    // steps still need to be done manually after first boot, since baking
    // real secrets (API keys, DB passwords) into user data would make them
    // visible in the EC2 console / instance metadata, which defeats the
    // point of keeping them out of source control in the first place.
    const userData = ec2.UserData.forLinux();
    userData.addCommands(
      "curl -fsSL https://get.docker.com -o get-docker.sh",
      "sh get-docker.sh",
      "usermod -aG docker ubuntu",
      `su - ubuntu -c "git clone ${props.githubRepoUrl} app"`,
      "echo 'Setup complete. SSH in, cd into the repo, create .env, then run: docker compose up -d' > /home/ubuntu/SETUP_NEXT_STEPS.txt",
      "chown ubuntu:ubuntu /home/ubuntu/SETUP_NEXT_STEPS.txt"
    );

    const instance = new ec2.Instance(this, "AppInstance", {
      vpc,
      vpcSubnets: { subnetType: ec2.SubnetType.PUBLIC },
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3A, ec2.InstanceSize.SMALL),
      machineImage,
      securityGroup,
      keyPair: ec2.KeyPair.fromKeyPairName(this, "KeyPair", props.keyPairName),
      userData,
      blockDevices: [
        {
          deviceName: "/dev/sda1",
          volume: ec2.BlockDeviceVolume.ebs(20, { volumeType: ec2.EbsDeviceVolumeType.GP3 }),
        },
      ],
    });

    // Elastic IP: keeps the public IP fixed across stop/start, so a nip.io
    // domain built from this IP doesn't change (and doesn't require a
    // frontend rebuild) every time the instance restarts.
    const eip = new ec2.CfnEIP(this, "AppElasticIp", {
      instanceId: instance.instanceId,
    });

    new cdk.CfnOutput(this, "InstancePublicIp", {
      value: eip.ref,
      description: "Elastic IP -- stays fixed across instance restarts",
    });

    new cdk.CfnOutput(this, "SuggestedNipIoDomain", {
      value: cdk.Fn.join("-", cdk.Fn.split(".", eip.ref)) + ".nip.io",
      description: "Use this as DOMAIN in your .env file",
    });

    new cdk.CfnOutput(this, "SshCommand", {
      value: `ssh -i "path/to/your-key.pem" ubuntu@${eip.ref}`,
    });
  }
}