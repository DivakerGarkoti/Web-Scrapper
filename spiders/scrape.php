<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

ini_set('log_errors', 1);
ini_set('error_log', 'C:\\xampp\\htdocs\\python project\\error.log'); 

header('Content-Type: application/json');

try {
    $python_interpreter = 'C:\\xampp\\htdocs\\python project\\project\\venv\\Scripts\\python.exe'; 

    $scrapy_project_dir = 'C:\\xampp\\htdocs\\python project\\cryptocurrency'; 

    if (!file_exists($python_interpreter)) {
        echo json_encode(['status' => 'error', 'message' => 'Python interpreter not found!']);
        exit;
    }

    if (!file_exists($scrapy_project_dir)) {
        echo json_encode(['status' => 'error', 'message' => 'Scrapy project directory not found!']);
        exit;
    }

    $command = 'cd ' . escapeshellarg($scrapy_project_dir) . ' && ' . escapeshellarg($python_interpreter) . ' -m scrapy crawl coinmarketcap 2>&1';

    exec($command, $output, $return_var);

    error_log('Output from command: ' . implode("\n", $output), 3, 'C:\\xampp\\htdocs\\python project\\error.log'); 

    if ($return_var === 0) {
        echo json_encode(['status' => 'success', 'message' => 'Scraping started successfully!', 'output' => $output]);
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Scrapy command failed to execute.', 'command' => $command, 'output' => $output]);
    }

} catch (Exception $e) {
    echo json_encode(['status' => 'error', 'message' => $e->getMessage()]);
}
?>
