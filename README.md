# farcaster

## tl;dr
There are two parts to this project.

The first is the docker image that actually runs the forecasting models.
It uses Dynamodb to read input and write output to.

The second part is the lambda function which takes the input time series, pushes it into Dynamodb and queues the ECS task
that will perform the forecast.

The docker image can be run locally if you can run a dynamodb docker image, and pass the required `ENV` variables to it.
### Directory `/fargate`
Builds a docker image that reads a json input from a file URL and generates a forecasted based on that time series.
Uses `fbProphet` library.
Default model used is `Prophet`. The Holt-Winters model provided by `statsmodels` is also available.
Use `./fargate/bin/build-docker-image` to build the docker image.

#### Deploy to ECR:
- Authenticate: `$(aws ecr get-login --no-include-email --region <your region>)`
- Build: `./fargate/bin/build-docker-image`
- Tag the image: `docker tag farcaster:latest <your account id>.dkr.ecr.<your region>.amazonaws.com/farcaster:latest`
- Push the image: `docker push <your account id>.dkr.ecr.<your region>.amazonaws.com/farcaster:latest`

#### Usage
Setup for local testing is not ready yet.

### Directory `/lambda`
Contains the configuration and setup for serverless deployment to AWS Lambda.

Requires a file called `config.dev.json` to have the configurations specific to your AWS account.

#### Deploy to Lambda
Navigate to `./lambda` and run `serverless package`.

Test what you need to.

When ready to deploy, `serverless deploy`.

### Issues
Have not figured out why the `dynamodb` permissions in `serverless.yml` are not being passed to the `ecsTaskExecutionRole`.
