<!DOCTYPE html>
<html>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<style>
input[type=text], select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

input[type=submit] {
  width: 100%;
  background-color: #4CAF50;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

input[type=submit]:hover {
  background-color: #45a049;
}

input[type=button] {
  width: 100%;
  background-color: #4cfa34;
  color: red;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}


div {
  border-radius: 5px;
  background-color: #f2f2f2;
  padding: 20px;
  margin: 10%;
}
</style>
<body  style="background-color:#E2D1F9;">

<h1 id="demo"></h1>

<div style="background-color: rgba(0,0,0,0.1);">
  <form method="post">
  <label for="Longitude"  id="ln"><h3>Longitude :</h3></label>
<input type="text" id="lgid"  name="lg"><br><br>

<label for="Latitude"><h3>Latitude :</h3></label>
<input type="text" id="ltid" name="lt"  ><br><br>

<label for="Housing age"><h3>Housing median<br> age :</h3></label>
<input type="text" id="haid" name="ha" ><br><br>

<label for="Total Rooms" ><h3>Total Rooms :</h3></label>
<input type="text" id="ocid" name="tr" ><br><br>

<label for="cars"><h3>Total Bedrooms :</h3></label>
<input type="text" id="tbid" name="tb" ><br><br>


<label for="Population"><h3>Population :</h3></label>
<input type="text" id="ppid" name="pp" ><br><br>

<label for="House Holds" ><h3>House Holds :</h3></label>
<input type="text" id="hhid" name="hh" ><br><br>

<label for="Income" ><h3>Median Income :</h3></label>
<input type="text" id="lnid" name="in"><br><br>

<label for="Ocean Proximity" ><h3>Ocean Proximity :</h3></label>
<select name="op" id="opid">
  <option value="Near Bays">Near Bay</option>
  <option value="Inland">Inland</option>
  <option value="Island">Island</option>
  <option value="Near Ocean">Near Ocean</option>
  <option value="<1H Ocean"> &lt1H Ocean</option>
</select>
<br>
<input type="submit" name="button1"  class="button" value="Submit" >
<br>
<input type="submit" name="button2" class="button"  style="color:red" value="exit">
  </form>



  <?php

if(isset($_POST["button1"])){
$Longitude = $_POST['lg'];
$Latitude = $_POST['lt'];
$Housing_median_age = $_POST['ha'];
$Total_rooms = $_POST['tr'];
$Total_bedrooms = $_POST['tb'];
$Population = $_POST['pp'];
$House_holds = $_POST['hh'];
$Median_income = $_POST['in'];
$Ocean_pro = $_POST['op'];
$conn = mysqli_connect('localhost','root','');
$db=mysqli_select_db($conn,"projects");
if($conn-> connect_error){
 die('connection failed : '.$conn->connect_error);
}
else{

    $query="select * from housing_results order by id desc limit 1";
          $query_run = mysqli_query($conn,$query);
          $row = mysqli_fetch_array($query_run);
          //echo $row['Results'];
   $stmt = $conn->prepare("insert into housing(Longitude, Latitude, Housing_median_age, Total_rooms, Total_bedrooms, Population, Households,  Median_income, Ocean_proximity)
            values(?,?,?,?,?,?,?,?,?)");
   $stmt->bind_param("dddiiiids",$Longitude,$Latitude,$Housing_median_age,$Total_rooms,$Total_bedrooms,$Population,$House_holds,$Median_income,$Ocean_pro);
   $stmt->execute();
   //echo "data entered successfully...";
   $stmt->close();
$x = 1;
$id=$row['ID'];
//set_time_limit(5);
while($x <= 5) {
$query="select * from housing_results order by id desc limit 1";
          $query_run = mysqli_query($conn,$query);
          $row = mysqli_fetch_array($query_run);
          if($row['ID']!=$id)
{
break;
}
//echo "The number is: $x <br>";
}
   echo $row['Results'];
   $conn->close();
}
}

else if(isset($_POST["button2"])){

shell_exec("start c:\\xampp\\xampp_stop.exe");

}
?>



</div>




  <!--<form method="post">
    <label for="Longitude" id="ln">L</label>
    <input type="text" id="fname" name="firstname" placeholder="Your name..">

    <label for="lname">Last Name</label>
    <input type="text" id="lname" name="lastname" placeholder="Your last name..">

    <label for="country">Country</label>
    <select id="country" name="country">
      <option value="australia">Australia</option>
      <option value="canada">Canada</option>
      <option value="usa">USA</option>
    </select>
  
    <input type="submit" name="button1" value="Submit">
  </form>-->


</body>
</html>


