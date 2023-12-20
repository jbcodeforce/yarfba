package org.acme;
import org.eclipse.microprofile.config.inject.ConfigProperty;

import software.amazon.awssdk.services.secretsmanager.model.CreateSecretRequest;
import software.amazon.awssdk.services.secretsmanager.model.GetSecretValueRequest;


public abstract class SecretsManagerResource {
    public static final String VERSION_STAGE = "AWSCURRENT";
    

    protected GetSecretValueRequest generateGetSecretValueRequest(String secretName) {
        return GetSecretValueRequest.builder() 
                .secretId(secretName)
                .versionStage(VERSION_STAGE)
                .build();
    }

    protected CreateSecretRequest generateCreateSecretRequest(SecretPayload secret) {
        return CreateSecretRequest.builder() 
                .name(secret.name)
                .secretString(secret.secret)
                .build();
    }
}
