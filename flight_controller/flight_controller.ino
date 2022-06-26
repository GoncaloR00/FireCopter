#include <Servo.h>
#include <Wire.h>

Servo L_F_prop;
Servo L_B_prop;
Servo R_F_prop;
Servo R_B_prop;

#define lf 9 //left front motor
#define lb 10 //left back motor
#define rf 11 //right front motor 
#define rb 3 //right back motor

//Variaveis de tempo
float elapsedTime, time, timePrev;

//Variaveis para o giroscopio
int gyro_error=0;                         //We use this variable to only calculate once the gyro data error
float Gyr_rawX, Gyr_rawY, Gyr_rawZ;       //Here we store the raw data read 
float Gyro_angle_x, Gyro_angle_y, Gyro_angle_z;         //Here we store the angle value obtained with Gyro data
float Gyro_raw_error_x, Gyro_raw_error_y, Gyro_raw_error_z; //Here we store the initial gyro data error

//Variaveis para o acelerometro
int acc_error=0;                            //We use this variable to only calculate once the Acc data error
float rad_to_deg = 180/3.141592654;         //This value is for pasing from radians to degrees values
float Acc_rawX, Acc_rawY, Acc_rawZ;         //Here we store the raw data read 
float Acc_angle_x, Acc_angle_y, Acc_angle_z;             //Here we store the angle value obtained with Acc data
float Acc_angle_error_x, Acc_angle_error_y, Acc_angle_error_z; //Here we store the initial Acc data error

float Total_angle_x, Total_angle_y, Total_angle_z;


//Variaveis para a velocidade dos motores
int MAX_SIGNAL = 2000; //Sinal máximo para o motor
int MIN_SIGNAL = 1000; //Sinal minimo para o motor
int MAX_Speed = 85; //Percentagem máxima da velocidade máxima do motor
int MIN_Speed = 10;
int lf_speed = 1000;
int rf_speed = 1000;
int lb_speed = 1000;
int rb_speed = 1000;
int Max_speed_val = 1500;
int Min_speed_val = 1500;

//Variaveis para os comandos
  //Input
int input_THROTTLE = 0; // 0 a 100
int input_YAW = 0; // -100 a 100
int input_ROLL = 0; // -100 a 100
int input_PITCH = 0; // -100 a 100
int input_ARM = 0;
int input_SOS = 0;
float ARM_time, SOS_time;
bool ARM = false;
bool ARMst = false;
bool SOS = false;
bool SOSst = false;
  //Output
int throttle = 1000;
int yaw = 0;
int pitch = 0;
int roll = 0;

//Variaveis para testes
int TEST=1100;
int i = 1;
bool up = true;

void setup() {
  Max_speed_val = 1850;
  Min_speed_val = MIN_SIGNAL + MIN_SIGNAL * MIN_Speed / 100;
  
//  delay(3000); //Dar tempo para ligar os ESC
  // Iniciar comunicação serial
  Serial.begin(115200);
  // Associar pinos aos ESC e evitar que estes entrem no modo de alteração de definições
  L_F_prop.attach(lf);
  L_F_prop.writeMicroseconds(MIN_SIGNAL);
  delay(10);
  L_B_prop.attach(lb);
  L_B_prop.writeMicroseconds(MIN_SIGNAL);
  delay(10);
  R_F_prop.attach(rf);
  R_F_prop.writeMicroseconds(MIN_SIGNAL);
  delay(10);
  R_B_prop.attach(rb);
  R_B_prop.writeMicroseconds(MIN_SIGNAL);
  delay(10);
  delay(7500); //Dar tempo para os ESC se configurarem

  Wire.begin();                           //begin the wire comunication
  // MPU-6050
  Wire.beginTransmission(0x68);           //begin, Send the slave adress (in this case 68)              
  Wire.write(0x6B);                       //make the reset (place a 0 into the 6B register)
  Wire.write(0x00);
  Wire.endTransmission(true);             //end the transmission
  
  Wire.beginTransmission(0x68);           //begin, Send the slave adress (in this case 68) 
  Wire.write(0x1B);                       //We want to write to the GYRO_CONFIG register (1B hex)
  Wire.write(0x10);                       //Set the register bits as 00010000 (100dps full scale)
  Wire.endTransmission(true);             //End the transmission with the gyro

  Wire.beginTransmission(0x68);           //Start communication with the address found during search.
  Wire.write(0x1C);                       //We want to write to the ACCEL_CONFIG register (1A hex)
  Wire.write(0x10);                       //Set the register bits as 00010000 (+/- 8g full scale range)
//  Wire.endTransmission(true);

//  // HMC5883
  Wire.beginTransmission(0x1E);
  Wire.write(0x02); //select mode register
  Wire.write(0x00); //continuous measurement mode
  Wire.endTransmission();
  Serial.print("HMC5883 done"); 

  time = millis();

  //Gyro error
  if(gyro_error==0)
  {
    for(int i=0; i<200; i++)
    {
      Wire.beginTransmission(0x68);            //begin, Send the slave adress (in this case 68) 
      Wire.write(0x43);                        //First adress of the Gyro data
      Wire.endTransmission(false);
      Wire.requestFrom(0x68,6,true);           //We ask for just 4 registers 
         
      Gyr_rawX=Wire.read()<<8|Wire.read();     //Once again we shif and sum
      Gyr_rawY=Wire.read()<<8|Wire.read();
      Gyr_rawZ=Wire.read()<<8|Wire.read();
   
      /*---X---*/
      Gyro_raw_error_x = Gyro_raw_error_x + (Gyr_rawX/32.8); 
      /*---Y---*/
      Gyro_raw_error_y = Gyro_raw_error_y + (Gyr_rawY/32.8);
      /*---Z---*/
      Gyro_raw_error_z = Gyro_raw_error_z + (Gyr_rawZ/32.8);
      if(i==199)
      {
        Gyro_raw_error_x = Gyro_raw_error_x/200;
        Gyro_raw_error_y = Gyro_raw_error_y/200;
        Gyro_raw_error_z = Gyro_raw_error_z/200;
        gyro_error=1;
      }
    }
  }//end of gyro error calculation
//  Serial.print("Gyro done"); 

  //Acc error
  if(acc_error==0)
  {
    for(int a=0; a<200; a++)
    {
      Wire.beginTransmission(0x68);
      Wire.write(0x3B);                       //Ask for the 0x3B register- correspond to AcX
      Wire.endTransmission(false);
      Wire.requestFrom(0x68,4,true); 
      
      Acc_rawX=(Wire.read()<<8|Wire.read())/4096.0 ; //each value needs two registres
      Acc_rawY=(Wire.read()<<8|Wire.read())/4096.0 ;
      Acc_rawZ=(Wire.read()<<8|Wire.read())/4096.0 ;

      
      /*---X---*/
      Acc_angle_error_x = Acc_angle_error_x + ((atan((Acc_rawY)/sqrt(pow((Acc_rawX),2) + pow((Acc_rawZ),2)))*rad_to_deg));
      /*---Y---*/
      Acc_angle_error_y = Acc_angle_error_y + ((atan(-1*(Acc_rawX)/sqrt(pow((Acc_rawY),2) + pow((Acc_rawZ),2)))*rad_to_deg)); 
      /*---Z---*/
      Acc_angle_error_z = Acc_angle_error_z + ((atan(-1*(Acc_rawX)/sqrt(pow((Acc_rawY),2) + pow((Acc_rawZ),2)))*rad_to_deg));
      if(a==199)
      {
        Acc_angle_error_x = Acc_angle_error_x/200;
        Acc_angle_error_y = Acc_angle_error_y/200;
        acc_error=1;
      }
    }
  }//end of acc error calculation
}

void loop() {
//  Medição do intervalo de tempo entre execuções
  timePrev = time;  // Atualizar instante da execução anterior
  time = millis();  // Guardar instante de execução
  elapsedTime = (time - timePrev) / 1000; // Obter intervalo de tempo em segundos

  //Obter comandos
  if(Serial.available()){
    String rxString = Serial.readStringUntil('\n');
    String strArr[6]; //Set the size of the array to equal the number of values you will be receiveing.
    //Keep looping until there is something in the buffer.
    int stringStart = 0;
    int arrayIndex = 0;
    for (int i=0; i < rxString.length(); i++){
      //Get character and check if it's our "special" character.
      if(rxString.charAt(i) == ','){
        //Clear previous values from array.
        strArr[arrayIndex] = "";
        //Save substring into array.
        strArr[arrayIndex] = rxString.substring(stringStart, i);
        //Set new string starting point.
        stringStart = (i+1);
        arrayIndex++;
      }
    }
    //Put values from the array into the variables.
    String v1 = strArr[0];
    String v2 = strArr[1];
    String v3 = strArr[2];
    String v4 = strArr[3];
    String v5 = strArr[4];
    String v6 = strArr[5];
    //Convert string to int if you need it.
    int aux_THROTTLE = v1.toInt();
    int aux_YAW = v2.toInt();
    int aux_PITCH = v3.toInt();
    int aux_ROLL = v4.toInt();
    input_THROTTLE = map(aux_THROTTLE,0,100,1000,2000);
    input_YAW = map(aux_YAW,-100,100,-10,10);
    input_PITCH = map(aux_PITCH,-100,100,-10,10);
    input_ROLL = map(aux_ROLL,-100,100,-10,10);
    input_ARM = v5.toInt();
    input_SOS = v6.toInt();
  }
  if ((input_ARM != 0) and (input_SOS != 0)) {
    input_ARM = 0;
  }
  if (input_ARM == 0){
    ARMst = false;
    ARM_time = 0;
  }
  if (!ARM and (input_ARM != 0)){
    if (!ARMst) {
      ARMst = true;
      ARM_time = time;
     }
    else {
      if ((time - ARM_time) >= 3000){
        ARM = true;
      }
    }
  }
  if (input_SOS == 0){
    SOSst = false;
    SOS_time = 0;
  }
  if (ARM and (input_SOS != 0)){
    if (!SOSst) {
      SOSst = true;
      SOS_time = time;
     }
    else {
      if ((time - SOS_time) >= 3000){
        ARM = false;
      }
    }
  }
  Serial.print("Throttle: ");
  Serial.print(input_THROTTLE);
  Serial.print(" Yaw: ");
  Serial.print(input_YAW);
  Serial.print(" Pitch: ");
  Serial.print(input_PITCH);
  Serial.print(" Roll: ");
  Serial.println(input_ROLL);
  // PID TEMPORARIO
  throttle = input_THROTTLE;
  yaw = input_YAW;
  pitch = input_PITCH;
  roll = input_ROLL;

  //Comandos de yaw, pitch e roll podem ir de -1000 a 1000
  //Limitar comandos para evitar movimentos bruscos
  if(throttle < 1000){throttle = 1000;}
  if(throttle > 2000){throttle = 2000;}
  if(yaw < -400){yaw = -400;}
  if(yaw > 400){yaw = 400;}
  if(pitch < -400){pitch = -400;}
  if(pitch > 400){pitch = 400;}
  if(roll < -400){yaw = -400;}
  if(roll > 400){yaw = 400;}
 
  //Obter velocidade de cada motor
  lf_speed = throttle + yaw + pitch + roll;
  rf_speed = throttle - yaw + pitch - roll;
  lb_speed = throttle - yaw - pitch + roll;
  rb_speed = throttle + yaw - pitch - roll;

  //Limitar velocidade dos motores
  if (lf_speed > Max_speed_val) {lf_speed = Max_speed_val;}
  if (lf_speed < Min_speed_val) {lf_speed = Min_speed_val;}
  if (rf_speed > Max_speed_val) {rf_speed = Max_speed_val;}
  if (rf_speed < Min_speed_val) {rf_speed = Min_speed_val;}
  if (lb_speed > Max_speed_val) {lb_speed = Max_speed_val;}
  if (lb_speed < Min_speed_val) {lb_speed = Min_speed_val;}
  if (rb_speed > Max_speed_val) {rb_speed = Max_speed_val;}
  if (rb_speed < Min_speed_val) {rb_speed = Min_speed_val;}
  
  if (ARM) {
    L_F_prop.writeMicroseconds(lf_speed);   
    L_B_prop.writeMicroseconds(lb_speed);
    R_F_prop.writeMicroseconds(rf_speed); 
    R_B_prop.writeMicroseconds(rb_speed);
  }
  if (!ARM){
    L_F_prop.writeMicroseconds(1000);   
    L_B_prop.writeMicroseconds(1000);
    R_F_prop.writeMicroseconds(1000); 
    R_B_prop.writeMicroseconds(1000);
  }

//  Serial.print("lf= "); Serial.print(lf_speed);
//  Serial.print(" lb= "); Serial.print(lb_speed);
//  Serial.print(" rf= "); Serial.print(rf_speed);
//  Serial.print(" rb= "); Serial.println(rb_speed);
//  Serial.print(Max_speed_val);
  
//  if ((TEST <= 1600) and up) {
//    Serial.print("UP ");
//    TEST = TEST + 1;
//    if (TEST > 1600) {
//      up = false;
//    }
//  }
//  if (!up) {
//    Serial.print("DOWN ");
//    TEST = TEST - 1;
//      if (TEST < 1101) {
//      up = true;
//      }
//  }
//  
//  L_F_prop.writeMicroseconds(TEST);   
//  L_B_prop.writeMicroseconds(TEST);
//  R_F_prop.writeMicroseconds(TEST); 
//  R_B_prop.writeMicroseconds(TEST);
//  Serial.println(TEST);

}
