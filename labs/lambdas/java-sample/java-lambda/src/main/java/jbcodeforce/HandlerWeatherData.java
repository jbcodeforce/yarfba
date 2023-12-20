package jbcodeforce;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class HandlerWeatherData implements RequestHandler<WeatherData,WeatherData>{
    static ObjectMapper mapper = new ObjectMapper();
    
    @Override
    public WeatherData handleRequest(WeatherData event, Context context) {

        LambdaLogger logger = context.getLogger();
        // process event
        event.setStatus("Processed");
        try {
            logger.log("EVENT: " + mapper.writeValueAsString(event));
        } catch(JsonProcessingException e) {
            e.printStackTrace();
        }
        logger.log("EVENT TYPE: " + event.getClass().toString());
        return event;
    }

    
}
