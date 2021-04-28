<?php

session_start();

function usernames(){
    echo "<select name=\"user\">
                <option value=\"false\">Who are you?</option>
                <option value=\"arabela/\">Arabela</option>
                <option value=\"chris/\">Chris</option>
                <option value=\"liam/\">Liam</option>
            </select>";
}
?>
<html>
    <head>
        <style>
            .dropdwn { cursor:pointer }
            .usr_dfnd_1 { display:none }
            .usr_dfnd_2 { display:none }
        </style>
    </head>
    <body style="font-family:'Verdana'">
    <!--<div style="right:40%;position:fixed;background-color:red;color:#fff;text-align:center;padding:10px;8px;font-weight:bold">Last SyncToy update:<br><? echo date('d/m/Y H:i:s',filemtime("../scripts/")); ?></div> -->
        <!--<a href="/" target="_self">Click to return to selection page</a>-->
        <h1>Scripts to speed stuff up.</h1>
        <h4><u>Click the rows below to expand them</u></h4>
        <p></p>
        <table style="width:1200px;border-collapse:collapse;font-size:13px">
            <tr>
                <td style="background-color:lightblue;padding:5px;border:1px solid #000">
                    <div class="dropdwn 1">
                        <p style="font-size:1em"><u><b>Status.asc cleanser</b></u></p>
                        <p></p>
                    </div>
                    <div class="divs div_1" style="display:none;font-size:1em">
                        <div style="padding:0px 0px 12px 0px"><code>This script removes all single pin nets from the Status.asc file.</code></div>
                        <form action="status_asc_cleanse.php" method="post" enctype="multipart/form-data" id="status" onsubmit="return status_vld()" class="all_forms">
                            <table style="border-collapse:collapse;font-size:13px">
                                <tr>
                                    <td style="font-weight:bold;border-bottom:1px solid #000">Choose file</td>
                                    <td style='border-bottom:1px solid #000'></td>
                                </tr><tr>
                                    <td colspan='2' style='padding-top:8px'></td>
                                </tr><tr>
                                    <td><input id="status_fl" type="file" name="dot_asc" /></td>
                                    <td><button id="but_status" name="but_cleanse" class="disable" disabled>SUBMIT</button></td>
                                </tr>
                            </table>
                        </form>
                    </div>
                </td>
            </tr><tr>
                <td style="padding:5px;border:1px solid #000">
                    <div class="dropdwn 2">
                        <p style="font-size:1em"><u><b>BOM versions</b></u></p>
                        <p></p>
                    </div>
                    <p></p>
                    <div class="divs div_2" style="display:none;font-size:1em">
                        <div style="padding:0px 0px 12px 0px"><code>Simply click the + button below to add new versions. "Version name" is populated with the name of the file you upload but you can change it. The "Grouped by part code" checkbox says whether any grouping shortcuts have been taken with components (<a href="pics/comp_shortcuts.jpg" target="_blank">see example</a>). "Comp. column" is the column where the component names are. "Parts column" [will probs be renamed to something clearer]. "Description" is the column holding the full description of the part (<a href="pics/description_column.jpg" target="_blank">see example</a>). "Row start" is the row the data starts on, not headings.</code></div>
                        <form action="cad_xy_split.php" method="post" enctype="multipart/form-data" class="all_forms" onsubmit="return parts_check()">
                            <table style="border-collapse:collapse;font-size:13px">
                                <tr>
                                    <td style='font-weight:bold;border-bottom:1px solid #000'>Choose Parts file</td>
                                    <td colspan="3" style='border-bottom:1px solid #000'>
                                        <table style='border-collapse:collapse;font-size:13px'>
                                            <tr style='font-weight:bold'>
                                                <td style="width:20px"></td>
                                                <td align="center" style="width:345px">Choose version file<span id="multiple_s" style="display:none">s</span></td>
                                                <td align="center" style="width:120px">Grouped by<br>part code</td>
                                                <td align="center" style="width:120px">Version name</td>
                                                <td align="center" style="width:70px;padding-left:8px">Components / Parts / Description</td>
                                                <td align="center" style="width:70px;padding-left:8px">Row start</td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr><tr>
                                    <td colspan='9' style='padding-top:8px'></td>
                                </tr><tr>
                                    <td style="vertical-align:top"><input type="file" name="parts_file" /></td>
                                    <td style="vertical-align:top"><span id="add_new" style="cursor:pointer"><img src="pics/add_new.png" /></span></td>
                                    <td id="append_holder" style="vertical-align:top"><table border="1" id="append_table" style="min-width:650px;border-collapse:collapse"></table></td>
                                    <td style="vertical-align:top"><button id="but_cad_xy" name="but_cad_xy" class="disable" disabled>SUBMIT</button></td>
                                </tr>
                            </table>
                        </form>
                    </div>
                </td>
            </tr><tr>
                <td style="padding:5px;background-color:lightgreen;border:1px solid #000">
                    <div class="dropdwn 3">
                        <p style="font-size:1em"><u><b>Pins file comparison</b></u></p>
                        <p></p>
                    </div>
                    <p></p>
                    <div class="divs div_3" style="display:none;font-size:1em">
                        <div style="padding:0px 0px 12px 0px"><code>This script compares two pins files to see where they differ. As Fabmaster and Tebo output slightly different results, you need to specify which software the pins files came from using the dropdown.</code></div>
                        <form action="comparison.php" method="post" enctype="multipart/form-data" class="all_forms">
                            <table style='border-collapse:collapse;font-size:13px'>
                                <tr style="font-weight:bold">
                                    <td style="padding-right:20px;border-bottom:1px solid #000">Choose Tebo or<br>Fabmaster</td>
                                    <td style="border-bottom:1px solid #000">Choose original pins file</td>
                                    <td style="border-bottom:1px solid #000">Choose new pins file</td>
                                    <td align="center" style="border-bottom:1px solid #000">User-defined<br>test points 1?</td>
                                    <td align="center" style="border-bottom:1px solid #000;width:80px;padding-left:10px">TP 1<br>prefix</td>
                                    <td align="center" style="border-bottom:1px solid #000;padding-left:10px">User-defined<br>test points 2?</td>
                                    <td align="center" style="border-bottom:1px solid #000;width:80px;padding-left:10px">TP 2 (e.g. vias)<br>prefix</td>
                                </tr><tr>
                                    <td colspan='3' style='padding-top:8px'></td>
                                </tr><tr>
                                    <td>
                                        <select id="tebo_fab" name="tebo_fab">
                                            <option value="false">Select...</option>
                                            <option value="fabmaster">Fabmaster</option>
                                            <option value="tebo">Tebo</option>
                                        </select>
                                    </td>
                                    <td><input type="file" id="original" name="original" /></td>
                                    <td><input type="file" id="new" name="new" /></td>
                                    <td align="center"><input type="checkbox" id="usr_dfnd_tp" name="usr_dfnd_tp" /></td>
                                    <td align="center" style="padding-left:10px;width:50px"><input class="usr_dfnd_1" type="text" name="usr_dfnd_1_txt" style="width:50px" /></td>
                                    <td align="center"><input class="usr_dfnd_1" type="checkbox" id="usr_dfnd_via" name="usr_dfnd_via" /></td>
                                    <td align="center" style="padding-left:10px;width:50px"><input class="usr_dfnd_2" type="text" name="usr_dfnd_2_txt" style="width:50px" /></td>
                                    <td style="padding-left:10px"><button id="but_comparison" name="but_comparison" class="disable" disabled>SUBMIT</button></td>
                                </tr>
                            </table>
                        </form>
                    </div>
                </td>
            </tr><tr>
                <td style="background-color:lightyellow;padding:5px;border:1px solid #000">
                    <div class="dropdwn 4">
                        <p style="font-size:1em"><u><b>Board X/Y plot generator</b></u></p>
                        <p></p>
                    </div>
                    <div class="divs div_4" style="display:none;font-size:1em">
                        <div style="padding:0px 0px 12px 0px"><code>This takes board_xy.asc files and splits them into top and bottom CADs. Please ensure you have a single empty line between sections, and no empty lines after section headings (<a href="pics/xy_plot_line_breaks.png" target="_blank">see example</a>).</code></div>
                        <form action="plot_gen.php" method="post" enctype="multipart/form-data" id="plot_gen" onsubmit="return plot_gen()" class="all_forms">
                            <table style='font-size:13px'>
                                <tr style="font-weight:bold">
                                    <td>Board type</td>
                                    <td>Choose file</td>
                                    <td>Input unit</td>
                                    <td>Output unit</td>
                                    <td></td>
                                </tr><tr>
                                    <td>
                                        <select id="plot_select" name="plot_select">
                                            <option value="false">Select...</option>
                                            <option value="single">Single board</option>
                                            <option value="panel">Panel</option>
                                            <option value="multi">Multi board</option>
                                            <option value="multi_panel">Multi Panel board</option>
                                        </select>
                                    </td>
                                    <td><input id="plot_file" type="file" name="plot_file" /></td>
                                    <td>
                                        <select id="input_measure" name="input_measure">
                                            <option value="inches">Inch</option>
                                            <option value="mm">Millimetre</option>
                                            <option value="thou">Thousandths of Inch</option>
                                            <option value="tenthou">Ten-thousandths of Inch</option>
                                        </select>
                                    </td>
                                    <td>
                                        <select id="output_measure" name="output_measure">
                                            <option value="inches">Inch</option>
                                            <option value="mm" disabled>Millimetre</option>
                                            <option value="thou" disabled>Thousandths of Inch</option>
                                            <option value="tenthou" disabled>Ten-thousandths of Inch</option>
                                        </select>
                                    </td>
                                    <td><button id="but_plot" name="but_plot" class="disable" disabled>SUBMIT</button></td>
                                </tr>
                            </table>
                        </form>
                    </div>
                </td>
            </tr><tr>
                <td style="background-color:#e5e4e2;padding:5px;border:1px solid #000">
                    <div class="dropdwn 5">
                        <p style="font-size:1em"><u><b>Find probe amount from Fabmaster @oldnail.asc</b></u></p>
                        <p></p>
                    </div>
                    <div class="divs div_5" style="display:none;font-size:1em">
                        <div style="padding:0px 0px 12px 0px"><code>This takes the @oldnail.asc file and tells you how many probe types.</code></div>
                        <form action="old_pins.php" method="post" enctype="multipart/form-data" id="old_pins" onsubmit="return old_pins()" class="all_forms">
                            <table style='font-size:13px;border-collapse:collapse'>
                                <tr style="font-weight:bold">
                                    <td style="font-weight:bold;border-bottom:1px solid #000">Choose file</td>
                                    <td style='border-bottom:1px solid #000'></td>
                                </tr><tr>
                                    <td><input id="old_pins_fl" type="file" name="old_pins_fl" /></td>
                                    <td><button id="but_old_pins" name="but_old_pins" class="disable" disabled>SUBMIT</button></td>
                                </tr>
                            </table>
                        </form>
                    </div>
                </td>
            </tr><tr>
                <td style="background-color:#ffd0aa;padding:5px;border:1px solid #000">
                    <div class="dropdwn 6">
                        <p style="font-size:1em"><u><b>Create files for Production</b></u></p>
                        <p></p>
                    </div>
                    <div class="divs div_6" style="display:none;font-size:1em">
                        <div style="padding:0px 0px 12px 0px"><code>Use the fields below to specify where the data you want is located in the fix-out file. You can do this by entering the row number of the start of your data and the row number of the end. If the data you need is split into numerous blocks over the file, you can add more start and end rows by clicking the + button.</code></div>
                        <form action="create_them.php" method="post" enctype="multipart/form-data" id="create_them" onsubmit="return create_them()" class="all_forms">
                            <table id="create_table" style='font-size:13px;border-collapse:collapse'>
                                <tr style="font-weight:bold">
                                    <td style="font-weight:bold;border-bottom:1px solid #000">Prefix code</td>
                                    <td style="font-weight:bold;border-bottom:1px solid #000;padding-left:8px">Choose fix-out file</td>
                                    <td style='border-bottom:1px solid #000'></td>
                                    <td style='border-bottom:1px solid #000;padding-left:8px'>Start row</td>
                                    <td style='border-bottom:1px solid #000;padding-left:8px'>End row</td>
                                    <td></td>
                                </tr><tr>
                                    <td colspan="6" style="padding-top:8px"></td>
                                </tr><tr>
                                    <td><input id="create_prefix" type="text" name="create_prefix" style="width:85px" /></td>
                                    <td style="padding-left:8px"><input id="create_fixout" type="file" name="create_fixout" /></td>
                                    <td style="vertical-align:top"><span id="add_new_create" style="cursor:pointer"><img src="pics/add_new.png" /></span></td>
                                    <td align="center" style="padding-left:8px"><input type="text" name="start[]" style="width:50px" /></td>
                                    <td align="center" style="padding-left:8px"><input type="text" name="end[]" style="width:50px" /></td>
                                    <!--FOR BUTTON BELOW class="disable" disabled-->
                                    <td><button id="but_create" name="but_create">SUBMIT</button></td>
                                </tr>
                            </table>
                        </form>
                    </div>
                </td>
            </tr><tr>
                <td style="background-color:#f2f8af;padding:5px;border:1px solid #000">
                    <div class="dropdwn 7">
                        <p style="font-size:1em"><u><b>Drill file split</b></u></p>
                        <p></p>
                    </div>
                    <div class="divs div_7" style="display:none;font-size:1em">
                        <div style="padding:0px 0px 12px 0px"><code>This script takes the drill file, modifies the coordinates so they match the orientation/measurement unit of the the Board XY, then creates .scr files for each probe size (100thou, etc.).</code></div>
                        <form action="drill_file.php" method="post" enctype="multipart/form-data" id="drill_file" onsubmit="return drill_file()" class="all_forms">
                            <table style='font-size:13px;border-collapse:collapse'>
                                <tr style="font-weight:bold">
                                    <td style="font-weight:bold;border-bottom:1px solid #000">Drill file</td>
                                    <td style="font-weight:bold;border-bottom:1px solid #000;padding-left:8px">Board XY</td>
                                    <td></td>
                                </tr><tr>
                                    <td colspan="6" style="padding-top:8px"></td>
                                </tr><tr>
                                    <td><input id="drill" type="file" name="drill" /></td>
                                    <td style="padding-left:8px"><input id="cad_xy" type="file" name="cad_xy" /></td>
                                    <td><button id="but_drill" name="but_drill" disabled>SUBMIT</button></td>
                                </tr>
                            </table>
                        </form>
                    </div>
                </td>
            </tr>
        </table>
            
    </body>
    <script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
    <script>
    var open_div = 0;
    var div_div = 0;
    var tebo_pins_num;
    var fabmaster_pins_num;
    var status_num;
        $(".dropdwn").click(function() {
            $(".disable").prop("disabled", true);
            tebo_pins_num = 0;
            fabmaster_pins_num = 0;
            status_num = 0;
            old_pins_num = 0;
            adding = 1;
            $("#multiple_s").hide();
            $("#append_holder").html("<table id=\"append_table\" style=\"min-width:650px\">");
            plot_okay = 0;
            if (open_div == 0){
                open_div = 1;
                div_div = $(this).attr('class').split(' ')[1];
                $(".divs").slideUp();
                $(".usr_dfnd_1").hide();
                $(".usr_dfnd_2").hide();
                $(".div_" + $(this).attr('class').split(' ')[1]).slideDown();
                $('.all_forms').trigger("reset");
            }else{
                if ($(this).attr('class').split(' ')[1] != div_div){
                    $(".divs").slideUp();
                    $(".usr_dfnd_1").hide();
                    $(".usr_dfnd_2").hide();
                    div_div = $(this).attr('class').split(' ')[1];
                    $(".div_" + $(this).attr('class').split(' ')[1]).slideDown();
                    $('.all_forms').trigger("reset");
                }else{
                    $(".divs").slideUp();
                    $(".usr_dfnd_1").hide();
                    $(".usr_dfnd_2").hide();
                    open_div = 0;
                    div_div = 0;
                    $('.all_forms').trigger("reset");
                }
            }
            
        });
        $("#status_fl").change(function (){
            ++status_num;
            if (status_num >= 1){
                $("#but_status").prop("disabled", false);
            }
        });
        $("#usr_dfnd_tp").change(function (){
            if ($(this).is(':checked')){
                $(".usr_dfnd_1").show();
            }else{
                $(".usr_dfnd_1").hide();
                $(".usr_dfnd_2").hide();
                $('#usr_dfnd_via').prop('checked', false);
            }
        });
        $("#usr_dfnd_via").change(function (){
            if ($(this).is(':checked')){
                $(".usr_dfnd_2").show();
            }else{
                $(".usr_dfnd_2").hide();
            }
        });
         $("#old_pins_fl").change(function (){
            ++old_pins_num;
            if (old_pins_num >= 1){
                $("#but_old_pins").prop("disabled", false);
            }
        });
        $("#tebo_fab").change(function(){
            if ($(this).val() == "false"){
                tebo_pins_num = (tebo_pins_num - 1);
                $("#but_comparison").prop("disabled", true);
            }else{
                ++tebo_pins_num;
                if (tebo_pins_num >= 3){
                    $("#but_comparison").prop("disabled", false);
                }
            }
        });
        $("#original").change(function (){
            ++tebo_pins_num;
            if (tebo_pins_num >= 3){
                $("#but_comparison").prop("disabled", false);
            }
        });
        $("#new").change(function (){
            ++tebo_pins_num;
            if (tebo_pins_num >= 3){
                $("#but_comparison").prop("disabled", false);
            }
        });
    </script>
    <script>
        adding = 1;
        $("#add_new").click(function() {
            if (adding > 1){
                $("#multiple_s").show();
            }
            if (adding == 1){ 
                $("#but_cad_xy").prop("disabled", false);
                $("#append_table").append("<tr><td style=\"font-size:13px\">Version " + adding + "</td><td style=\"width:270px\"><input type=\"file\" id=\"version_csv_" + adding + "\" name=\"version_csv_" + adding + "\" class=\"version_but " + adding +"\" /><input type=\"hidden\" name=\"hiddens[]\" value=\"" + adding + "\" /></td><td align=\"center\" style=\"font-size:13px;width:123px\"><input type=\"checkbox\" name=\"file_type" + adding + "\" /><td align=\"center\" style=\"width:123px\"><input type=\"text\" id=\"version_num" + adding + "\" name=\"version_num" + adding + "\" style=\"width:100px\" class=\"versions\" /></td><td align=\"center\" style=\"width:30px\"><input type=\"text\" name=\"component_name" + adding + "\" style=\"width:30px;text-transform:uppercase\" class=\"components\" /></td><td align=\"center\" style=\"width:30px\"><input type=\"text\" name=\"part_num" + adding + "\" style=\"width:30px;text-transform:uppercase\" class=\"parts\" /></td><td align=\"center\" style=\"width:30px\"><input type=\"text\" name=\"desc" + adding + "\" style=\"width:30px;text-transform:uppercase\" class=\"parts\" /></td><td align=\"center\" style=\"width:73px\"><input type=\"text\" name=\"data_starts" + adding + "\" style=\"width:60px\" class=\"starts\" /></td></tr>");
            }else{
                $("#append_table").append("<tr id=\"remove_tr" + adding + "\"><td style=\"font-size:13px\">Version " + adding + "</td><td style=\"width:270px\"><input type=\"file\" id=\"version_csv_" + adding + "\" name=\"version_csv_" + adding + "\" class=\"version_but " + adding +"\" /><input type=\"hidden\" name=\"hiddens[]\" value=\"" + adding + "\" /></td><td align=\"center\" style=\"font-size:13px\"><input type=\"checkbox\" name=\"file_type" + adding + "\" /></td><td align=\"center\"><input type=\"text\" id=\"version_num" + adding + "\" name=\"version_num" + adding + "\" style=\"width:100px\" class=\"versions\" /></td><td align=\"center\"><input type=\"text\" name=\"component_name" + adding + "\" style=\"width:30px;text-transform:uppercase\" class=\"components\" /></td><td align=\"center\"><input type=\"text\" name=\"part_num" + adding + "\" style=\"width:30px;text-transform:uppercase\" class=\"parts\" /></td><td align=\"center\" style=\"width:30px\"><input type=\"text\" name=\"desc" + adding + "\" style=\"width:30px;text-transform:uppercase\" class=\"parts\" /></td><td align=\"center\"><input type=\"text\" name=\"data_starts" + adding + "\" style=\"width:60px\" class=\"starts\" /></td><td><img id=\"remove" + adding + "\" class=\"remove_it\" src=\"pics/remove.png\" style=\"cursor:pointer\" /></td></tr>");
                if (adding > 2){
                    $("#remove" + (adding - 1)).hide();
                }
            }
            adding++; 
        });
        $(document).on('click','.remove_it',function (){
            $("#remove_tr" + (adding - 1)).remove();
            $("#remove" + (adding - 2)).show();
            if ($('#remove_tr').length == 0) {
              adding--;
            }
        });
        $(document).on('change','.version_but',function (){
            var fileName = $(this).val().replace(/\.[^/.]+$/, "");
            fileName = fileName.replace("C:\\fakepath\\","");
            $('#version_num' + $(this).attr('class').split(' ')[1]).val(fileName);
        });
        function parts_check(){
            var versions_blank = 0;
            var comp_blank = 0;
            var parts_blank = 0;
            var starts_blank = 0;
            var any_errors = 0;
            var versions_arr = [];
            $('.versions').each(function(i, obj) { 
                if ($(this).val() == ""){ 
                    ++versions_blank; 
                }else{ 
                    versions_arr.push($(this).val());
                } 
            });
            $('.components').each(function(i, obj) { 
                if ($(this).val() == ""){ 
                    ++comp_blank; 
                } 
            }); 
            $('.parts').each(function(i, obj) { 
                if ($(this).val() == ""){ 
                    ++parts_blank; 
                } 
            }); 
            $('.starts').each(function(i, obj) { 
                if ($(this).val() == ""){ 
                    ++starts_blank; 
                } 
            }); 
            if (versions_blank > 0){ 
                var vers_msg = "\u2022 You can't leave Version name blank.\n"; 
                ++any_errors; 
            }else{ 
                var vers_msg = "";
            } 
            if (comp_blank > 0){ 
                var comp_msg = "\u2022 You can't leave Component column blank.\n"; 
                ++any_errors; 
            }else{ 
                var comp_msg = ""; 
            } 
            if (parts_blank > 0){ 
                var part_msg = "\u2022 You can't leave Parts column blank.\n"; 
                ++any_errors; 
            }else{ 
                var part_msg = ""; 
            } 
            if (starts_blank > 0){ 
                var start_msg = "\u2022 You can't leave Row start blank.\n"; 
                ++any_errors; 
            }else{ 
                var start_msg = ""; 
            } var uniqueNames = []; 
                $.each(versions_arr, function(i, el){ 
                if($.inArray(el, uniqueNames) === -1) uniqueNames.push(el); 
            }); 
            if (uniqueNames.length < (adding - 1)){ 
                var dupes = "\u2022 You have duplicate Version names.\n"; 
                ++any_errors; 
            }else{ 
                var dupes = ""; 
            } 
            if (any_errors > 0){ 
                alert (vers_msg + comp_msg + part_msg + start_msg + dupes); 
                return false; 
            }else{ 
                return confirm("Are you sure you've uploaded the correct files? If yes, click OK.");
            } 
        }
    </script>
    <script>
    drill_file_count = 0;
        $("#drill").change(function (){
            ++drill_file_count;
            if (drill_file_count >= 2){
                $("#but_drill").prop("disabled", false);
            }
        });
        $("#cad_xy").change(function (){
            ++drill_file_count;
            if (drill_file_count >= 2){
                $("#but_drill").prop("disabled", false);
            }
        });
    </script>
    <script>
        $("#add_new_create").click(function() {
            $("#create_table").append("</tr><tr><td></td><td></td><td></td><td align=\"center\" style=\"padding-left:8px\"><input type=\"text\" name=\"start[]\" style=\"width:50px\" /></td><td align=\"center\" style=\"padding-left:8px\"><input type=\"text\" name=\"end[]\" style=\"width:50px\" /></td><td></td></tr>");
        });
    </script>
    <script>
        var plot_okay = 0;
        var select_one = 0;
        $("#plot_select").change(function (){
            if ($(this).val() != "false"){
                if (select_one == 0){
                    ++plot_okay;
                    ++select_one;
                    if (plot_okay == 2){
                        $("#but_plot").prop("disabled", false);
                    }
                }
            }else{
                --plot_okay;
                select_one = 0
                $("#but_plot").prop("disabled", true);
            }
        });
        $("#plot_file").change(function (){
            ++plot_okay;
            if (plot_okay == 2){
                $("#but_plot").prop("disabled", false);
            }
        });
    </script>
    <?php 
        if (isset($_SESSION['script_complete'])){
        ?><script></script><?php
            unset($_SESSION['script_complete']);
        } 
    ?>
</html>