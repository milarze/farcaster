# farcaster

## tl;dr
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
Build Docker image
```
bin/build-docker-image
```

Run docker
```
docker run -e INPUT_JSON_KEY=<file_key> -e S3_BUCKET=farcaster MODEL=<prophet or statsmodels> farcaster
```

Input JSON file format
```
{
  "time_series": [
    {
      "date": "2019-02-21",
      "quantity":20.0
    }
    ...
  ],
  "aggregation": "day" // day, week or month
}
```

### Directory `/lambda`
Contains the configuration and setup for serverless deployment to AWS Lambda.

Requires a file called `config.dev.json` to have the configurations specific to your AWS account.

#### Deploy to Lambda
Navigate to `./lambda` and run `serverless package`.
Test what you need to.
When ready to deploy, `serverless deploy`.

### Issues
Have not figured out why the `dynamodb` permissions in `serverless.yml` are not being passed to the `ecsTaskExecutionRole`.
