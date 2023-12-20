package jbcodeforce;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;

/**
 * Unit test for simple App.
 */
public class AppTest {
    
  @Test
  void invokeTest() {
    WeatherData event = new WeatherData();
    event.setHumidityPct(.6);
    Context context = new MockContext();
    HandlerWeatherData handler = new HandlerWeatherData();
    WeatherData result = handler.handleRequest(event, context);
    assertEquals("Processed",result.getStatus());
  }
}
