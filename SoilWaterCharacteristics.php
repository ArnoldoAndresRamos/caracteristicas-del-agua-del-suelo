<?php

function swc(S,C,MO){

	function humedad_1500_KPa(){
        $Q1500t = -0.024*S+0.487*C+0.006*MO+0.005*(S*MO)-0.013*(C*MO)+0.068*(S*C)+0.031;
		return $Q1500t;
	};

	echo swc(3,2,1);


}

?>