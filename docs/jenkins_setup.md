# Setting Up Jenkins for Conversation Extractor

This guide explains how to set up a Jenkins pipeline for the Conversation Extractor project.

## Prerequisites

1. Jenkins server installed and running
2. Jenkins Pipeline plugin installed
3. Python installed on the Jenkins server or agent

## Setting Up the Pipeline

### Option 1: Using the Jenkins UI

1. **Create a new Pipeline job**:
   - Go to Jenkins dashboard
   - Click "New Item"
   - Enter a name (e.g., "conversation-extractor")
   - Select "Pipeline"
   - Click "OK"

2. **Configure the Pipeline**:
   - In the "Pipeline" section, select "Pipeline script from SCM"
   - Select "Git" as the SCM
   - Enter your repository URL (e.g., `https://github.com/washyu/conversation-extractor.git`)
   - Specify the branch to build (e.g., `*/main`)
   - Set the Script Path to `Jenkinsfile` (or `Jenkinsfile.no-docker` if not using Docker)
   - Click "Save"

3. **Run the Pipeline**:
   - Click "Build Now" to run the pipeline

### Option 2: Using the Jenkins CLI

1. **Create a job configuration XML file** (save as `conversation-extractor-job.xml`):

```xml
<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@2.40">
  <description>Pipeline for building and testing the Conversation Extractor package</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty>
      <triggers>
        <hudson.triggers.SCMTrigger>
          <spec>H/15 * * * *</spec>
          <ignorePostCommitHooks>false</ignorePostCommitHooks>
        </hudson.triggers.SCMTrigger>
      </triggers>
    </org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty>
  </properties>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition" plugin="workflow-cps@2.90">
    <scm class="hudson.plugins.git.GitSCM" plugin="git@4.7.1">
      <configVersion>2</configVersion>
      <userRemoteConfigs>
        <hudson.plugins.git.UserRemoteConfig>
          <url>https://github.com/washyu/conversation-extractor.git</url>
        </hudson.plugins.git.UserRemoteConfig>
      </userRemoteConfigs>
      <branches>
        <hudson.plugins.git.BranchSpec>
          <name>*/main</name>
        </hudson.plugins.git.BranchSpec>
      </branches>
      <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
      <submoduleCfg class="empty-list"/>
      <extensions/>
    </scm>
    <scriptPath>Jenkinsfile</scriptPath>
    <lightweight>true</lightweight>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>
```

2. **Create the job using the Jenkins CLI**:

```bash
java -jar jenkins-cli.jar -s http://your-jenkins-server create-job conversation-extractor < conversation-extractor-job.xml
```

## Configuring Webhooks

To automatically trigger builds when changes are pushed to GitHub:

1. **In Jenkins**:
   - Install the "GitHub Integration" plugin
   - Go to "Manage Jenkins" > "Configure System"
   - Scroll to the "GitHub" section
   - Add GitHub server configuration
   - Save

2. **In GitHub**:
   - Go to your repository
   - Click "Settings" > "Webhooks" > "Add webhook"
   - Set Payload URL to `http://your-jenkins-server/github-webhook/`
   - Select "application/json" as content type
   - Choose which events should trigger the webhook
   - Click "Add webhook"

## Using the Built Artifacts

After a successful build, you can:

1. **Download the artifacts** from the Jenkins build page
2. **Install the package** directly:
   ```bash
   pip install /path/to/downloaded/conversation_extractor-0.1.0-py3-none-any.whl
   ```
3. **Use in requirements.txt** with a direct link to the Jenkins artifact:
   ```
   conversation-extractor @ http://your-jenkins-server/job/conversation-extractor/lastSuccessfulBuild/artifact/dist/conversation_extractor-0.1.0-py3-none-any.whl
   ```

## Troubleshooting

### Common Issues

1. **Missing dependencies**:
   - Ensure Python and required packages are installed on the Jenkins agent
   - Check that the `setup.py` file includes all necessary dependencies

2. **Permission issues**:
   - Ensure the Jenkins user has permission to create virtual environments
   - Check file permissions for the workspace directory

3. **NLTK data download failures**:
   - Ensure Jenkins has internet access
   - Consider pre-downloading NLTK data and mounting it as a volume

### Viewing Logs

1. Go to the build in Jenkins
2. Click on "Console Output" to see the full build log
3. Check for error messages or failed steps
