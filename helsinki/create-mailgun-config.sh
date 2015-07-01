#!/bin/bash

if [ -z "$MAILGUN_API_KEY" ]; then
  echo "MAILGUN_API_KEY is not set"
  exit 1;
fi

if [ -z "$MAILGUN_SANDBOX_ID" ]; then
  echo "MAILGUN_SANDBOX_ID is not set"
  exit 1;
fi

echo "{
  \"key\": \"$MAILGUN_API_KEY\",
  \"post_url\": \"https://api.mailgun.net/v3/$MAILGUN_SANDBOX_ID\",
  \"sandbox\": \"$MAILGUN_SANDBOX_ID\"
}"
