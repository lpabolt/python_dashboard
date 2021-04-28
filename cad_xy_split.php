<?php

session_start();

//$main_filename = strtolower(str_replace(" ","_",$_POST['flnm']));

//$destination_file = $main_filename . "_" . time();
/* move_uploaded_file($_FILES['cad_xy_flnm']['tmp_name'],"cad_xy.txt");
fopen($destination_file . "cad_xy_edited.txt", "w"); */

$versions_uploaded = (count($_FILES) - 1);

move_uploaded_file($_FILES['parts_file']['tmp_name'],"OUTPUTS\Parts.asc");

$filenames = "";

for ($acb = 0;$acb < $versions_uploaded;$acb++){
    move_uploaded_file($_FILES['version_csv_' . ($acb + 1)]['tmp_name'],"OUTPUTS\\" . $_FILES['version_csv_' . ($acb + 1)]['name']);
    $filenames  .= $_FILES['version_csv_' . ($acb + 1)]['name'] . " ";
}

$exec_str = "";
for ($abc = 0;$abc < $versions_uploaded;$abc++){
    $exec_str .= $_POST['version_num' . ($abc + 1)] . " " . strtoupper($_POST['component_name' . ($abc + 1)]) . " " . strtoupper($_POST['part_num' . ($abc + 1)]) . " " . strtoupper($_POST['desc' . ($abc + 1)]) . " " . $_POST['data_starts' . ($abc + 1)] . " " . $_POST['file_type' . ($abc + 1)] . " ";
}

$tmp = exec('python strip_parts.py 2>&1',$my_output);

$tmp = exec('python build_xy.py ' . $versions_uploaded . ' ' . $exec_str . ' ' . $filenames . '2>&1',$my_output);

var_dump($my_output);

exec('start OUTPUTS');
//to force open
exec('start OUTPUTS');

//header ("Location: /scripts/");
