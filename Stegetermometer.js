var adcVal = msg.payload;

//Nedenstående kode er en linær udregning af temp.
//Problemet med den er, at den ikke tager højde for afvigelser
// ift. variationer i temp værdiernes adc værdi i forhold til hinanden.
/*
//beregner spænding
    var volts = (adcVal * 3.3) / 1023;

//beregner spænding https://dev.to/adamkdean/spi-with-mcp3008-adc-chip-tmp36-analogue-temp-sensor-b3c
    var tempC = volts * 12.22;

msg.payload = tempC;
110.8*10^-0.003
*/

//Her bruger vi vores funktion fra excel arket, til at tilnærme os en temperatur
//ved at erstatte x med vores adc værdi.
//Math.pow er en måde at opløfte et tal i et andet. Math.E er eulers tal.
//msg.payload = 110.8*Math.pow(Math.E , -0.003 * adcVal);


msg.payload = 116.36*Math.pow(Math.E , -0.003 * adcVal);
return msg;