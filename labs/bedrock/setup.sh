export AWS_DEFAULT_REGION=us-west-2
echo "(Re)-creating directory"
rm -rf ./dependencies
mkdir ./dependencies
cd ./dependencies
echo "Downloading dependencies"
curl -sS https://d2eo22ngex1n9g.cloudfront.net/Documentation/SDK/bedrock-python-sdk.zip > sdk.zip
echo "Unpacking dependencies"
# (SageMaker Studio system terminals don't have `unzip` utility installed)
if command -v unzip &> /dev/null
then
    unzip sdk.zip && rm sdk.zip && echo "Done"
else
    echo "'unzip' command not found: Trying to unzip via Python"
    python -m zipfile -e sdk.zip . && rm sdk.zip && echo "Done"
fi

pip install --upgrade pip
pip install --no-build-isolation --force-reinstall \
    ./dependencies/awscli-*-py3-none-any.whl \
    ./dependencies/boto3-*-py3-none-any.whl \
    ./dependencies/botocore-*-py3-none-any.whl
pip install -r ./requirements.txt