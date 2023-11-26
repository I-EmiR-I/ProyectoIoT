<?php
$servername = "";
$username = "";
$password = "";
$dbname = "";

try {
    $conn = new PDO("connection string", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Verificar si se proporcionaron los parámetros en la URL
    if (isset($_GET['latitud']) && isset($_GET['longitud']) && isset($_GET['embarcacionID']) && isset($_GET['idSensor'])) {
        // Agregar datos a la tabla de SensoresGPS
        $stmt = $conn->prepare("INSERT INTO SensoresGPS (Latitud, Longitud, FechaMedicion, EmbarcacionID, id) VALUES (:latitud, :longitud, :fecha, :embarcacionID, :id)");
        $stmt->bindParam(':latitud', $latitud);
        $stmt->bindParam(':longitud', $longitud);
        $stmt->bindParam(':fecha', $fecha);
        $stmt->bindParam(':embarcacionID', $embarcacionID);
        $stmt->bindParam(':id', $idSensor);

        // Asignar valores a las variables desde la URL
        $latitud = $_GET['latitud'];
        $longitud = $_GET['longitud'];
        $fecha = date('Y-m-d H:i:s');
        $embarcacionID = $_GET['embarcacionID'];
        $id = $_GET['idSensor'];

        // Ejecutar la consulta
        $stmt->execute();

        echo "Datos de GPS insertados correctamente.";
    } else {
        echo "Falta uno o más parámetros en la URL.";
    }
} catch (PDOException $e) {
    echo "Error: " . $e->getMessage();
}

$conn = null;
?>
