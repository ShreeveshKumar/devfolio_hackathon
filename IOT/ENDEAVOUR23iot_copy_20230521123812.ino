
int val1 = 0 ; 
 int val2=0; 
 int c=0;
 void setup()  
 {  
   Serial.begin(9600);   
   pinMode(14,HIGH);      
 }  
 void loop()   
 {  
  val1 = digitalRead(D1);   
  val2 = digitalRead(D3);
  Serial.println(c);   
  delay(350);       
  if(val1 == 0 )  
 {  
   digitalWrite(D5,HIGH);   
   c++;
  }  
  else
  {  
   digitalWrite(D5,LOW);  
  } 
  
 if(val2 == 0)  
  {  
   digitalWrite(D6,HIGH); 
   c--; 
  }  
  else
  {  
   digitalWrite(D6,LOW);   
  }   
}