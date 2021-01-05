<?php


function swc($S,$C,$MO){

	function humedad_1500_KPa()
	{
        	$Q1500t = -0.024*$S+0.487*$C+0.006*$MO+0.005*($S*$MO)-0.013*($C*$MO)+0.068*($S*$C)+0.031;
		return $Q1500+ (0.14 * $Q1500t -0.02);
	};
	#echo humedad_1500_KPa();

	function humedad_33_KPa(){
		$Q33t = -0.251*$S+0.195*$C+0.011*$MO+0.006*($S*$MO)-0.027*($C*$MO)+0.452*($S*$C)+0.299;
		return $Q33t +(1.283*($Q33t * $Q33t)-0.374*($Q33t)-0.015);
	};
	return "Q1500: ".humedad_1500_KPa()."<br>"." Q33: ".humedad_33_KPa();	
};

echo swc(0.2,0.2,2.5);

?>
