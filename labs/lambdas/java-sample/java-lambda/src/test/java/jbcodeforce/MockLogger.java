package jbcodeforce;
import java.util.logging.Logger;

import com.amazonaws.services.lambda.runtime.LambdaLogger;

public class MockLogger  implements LambdaLogger {
        private static final Logger logger = Logger.getLogger("TestLogger");
        
        public void log(String message){
          logger.info(message);
        }
        public void log(byte[] message){
          logger.info(new String(message));
        }
}
