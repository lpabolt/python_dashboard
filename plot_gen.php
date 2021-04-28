<?php

//  don't have to worry about this just yet, but just define it early on
if (isset($_POST['zener'])){
    $is_zener = 1;
}else{
    $is_zener = 0;
}

move_uploaded_file($_FILES['plot_file']['tmp_name'],"OUTPUTS\board_xy.asc");

$tmp = exec('python board_xy_plotter.py ' . $_POST['plot_select'] . ' ' . $_POST['input_measure'] . ' ' . $_POST['output_measure'] . ' 2>&1',$my_output);

var_dump($my_output);

exec('start .\OUTPUTS');
//to force open
exec('start .\OUTPUTS');

header ("Location: /scripts/");