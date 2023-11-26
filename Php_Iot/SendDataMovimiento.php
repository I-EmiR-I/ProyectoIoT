<?php
$servername = "";
$username = "";
$password = "";
$dbname = "";

try {
    $conn = new PDO("connection string", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Verificar si se proporcionaron los parámetros en la URL
    if (isset($_GET['movimientoDetectado']) && isset($_GET['embarcacionID']) && isset($_GET['idSensor'])) {
        // Agregar datos a la tabla de SensoresMovimiento
        $stmt = $conn->prepare("INSERT INTO SensoresMovimiento (MovimientoDetectado, FechaMedicion, EmbarcacionID, id) VALUES (:movimientoDetectado, :fecha, :embarcacionID, :id)");
        $stmt->bindParam(':movimientoDetectado', $movimientoDetectado);
        $stmt->bindParam(':fecha', $fecha);
        $stmt->bindParam(':embarcacionID', $embarcacionID);
        $stmt->bindParam(':id', $idSensor);

        // Asignar valores a las variables desde la URL
        $movimientoDetectado = $_GET['movimientoDetectado'];
        $fecha = date('Y-m-d H:i:s');
        $embarcacionID = $_GET['embarcacionID'];
        $id = $_GET['idSensor'];

        // Ejecutar la consulta
        $stmt->execute();

        echo "Datos de Movimiento insertados correctamente.";
    } else {
        echo "Falta uno o más parámetros en la URL.";
    }
} catch (PDOException $e) {
    echo "Error: " . $e->getMessage();
}

$conn = null;
?>
