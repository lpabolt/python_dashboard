<?php

session_start();

move_uploaded_file($_FILES['dot_asc']['tmp_name'],"OUTPUTS\Status.asc");
fopen("OUTPUTS\Cust_Status.asc", "w");

$tmp = exec('python create_cust_status.py 2>&1',$my_output);

//unlink("OUTPUTS\Status.asc");

exec('start .\OUTPUTS');
//to force open
exec('start .\OUTPUTS');

header ("Location: /scripts/");