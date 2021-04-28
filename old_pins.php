<?php

move_uploaded_file($_FILES['old_pins_fl']['tmp_name'],"@oldnail.asc");

$tmp = exec('python old_pins.py 2>&1',$my_output);

foreach ($my_output as $a){
    if ($a == "BOTTOM"){
        echo "<b>" . $a . "</b>";
    }else{
        if ($a == "TOP"){
            echo "<br><b>" . $a . "</b>";
        }else{
            echo $a . "<br>";
        }
    }
}

unlink("@oldnail.asc");

echo "<br><br><a href=\"../scripts/\" target=\"_self\">Click to go back</a>";