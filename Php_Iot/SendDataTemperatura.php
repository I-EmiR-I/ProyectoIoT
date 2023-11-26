<?php
$servername = "puenteacero-server.database.windows.net";
$username = "admin123";
$password = "PuenteAcero123!";
$dbname = "InventariosPuenteAcero";

try {
    $conn = new PDO("sqlsrv:server = tcp:puenteacero-server.database.windows.net,1433; Database = InventariosPuenteAcero", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Verificar si se proporcionaron los parámetros en la URL
    if (isset($_GET['temperatura']) && isset($_GET['embarcacionID'])) {
        // Obtener el valor del parámetro id de la URL
        $idSensor = isset($_GET['idSensor']) ? $_GET['idSensor'] : null;

        // Agregar datos a la tabla de SensoresTemperatura
        $stmt = $conn->prepare("INSERT INTO SensoresTemperatura (id, Temperatura, FechaMedicion, EmbarcacionID) VALUES (:id, :temperatura, :fecha, :embarcacionID)");
        $stmt->bindParam(':id', $idSensor, PDO::PARAM_INT);
        $stmt->bindParam(':temperatura', $temperatura);
        $stmt->bindParam(':fecha', $fecha);
        $stmt->bindParam(':embarcacionID', $embarcacionID);

        // Asignar valores a las variables desde la URL
        $temperatura = $_GET['temperatura'];
        $fecha = date('Y-m-d H:i:s'); // Obtener la fecha y hora actual
        $embarcacionID = $_GET['embarcacionID'];

        // Ejecutar la consulta
        $stmt->execute();

        echo "Datos insertados correctamente.";
    } else {
        echo "Falta uno o más parámetros en la URL.";
    }
} catch(PDOException $e) {
    echo "Error: " . $e->getMessage();
}

$conn = null;
?>
