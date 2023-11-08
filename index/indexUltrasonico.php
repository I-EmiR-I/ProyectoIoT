<?php
	$Datos = $_GET["Datos"];
	//$Datos2 = $_GET["Datos2"];

	$usuario = "root";
	$contrasena = "";
	$servidor = "localhost";
	$basededatos = "basededatos";

	$conexion = mysqli_connect( $servidor, $usuario, "" ) or die ("No se ha podido conectar al servidor de base de datos");

	$db = mysqli_select_db( $conexion, $basededatos ) or die ("No se ha podido seleccionar la base de datos");

	$fecha = date("Y-m-d H:i:s");  // Get the current date and time in the format "YYYY-MM-DD HH:MM:SS"

    $consulta = "INSERT INTO sensoresultrasonico (Distancia, Fecha) VALUES (" . $Datos . ", '" . $fecha . "')";
	
	$resultado = mysqli_query( $conexion, $consulta );
	if ($resultado) {
		echo "Datos insertados correctamente.";
	} else {
		echo "Error al insertar datos: " . mysqli_error($conexion);
	}
?>
