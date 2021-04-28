<?php

ini_set('max_execution_time', 300);

echo "Began " . date('H:i:s',time()) . "<br><br>";

$tmp = exec('python tester2.py 2>&1',$my_output);

echo "Ended " . date('H:i:s',time());

//remove this after testing
var_dump($my_output);