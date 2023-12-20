package org.acme;

import java.util.List;

import org.eclipse.microprofile.config.inject.ConfigProperty;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import software.amazon.awssdk.services.secretsmanager.SecretsManagerClient;
import software.amazon.awssdk.services.secretsmanager.model.SecretListEntry;

@ApplicationScoped
@Path("/secrets")
public class SecretsResource extends SecretsManagerResource {
    @ConfigProperty(name = "secret.name") 
    String secretName;


    @Inject 
    SecretsManagerClient secretsManagerClient;

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public String hello() {
       
        return "Hello with secret: " + secretsManagerClient.getSecretValue(generateGetSecretValueRequest(secretName)).secretString();
    }

    @GET
    @Path("/{name}")
    @Produces(MediaType.APPLICATION_JSON)
    public String hello(String name) {
       
        return "Hello with secret: " + secretsManagerClient.getSecretValue(generateGetSecretValueRequest(name)).secretString();
    }

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    @Path("/list")
    public    String listSecrets() {
        List<SecretListEntry> rep = secretsManagerClient.listSecrets().secretList();
        if (rep!= null && !rep.isEmpty()) {
            return rep.toString();
        }
        return "Nothing";
    }

    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    public void createSecret(SecretPayload secret) {
        System.out.println(secret);
        System.out.println(secretsManagerClient.createSecret(generateCreateSecretRequest(secret)));
    }
}
