<?php
function esPerfecto($numero) {
    $suma = 0;
    for ($i = 1; $i < $numero; $i++) {
        if ($numero % $i == 0) {
            $suma += $i;
        }
    }
    return $suma == $numero;
}

function mostrarNumerosPerfectos($limite) {
    echo "Números perfectos hasta $limite:\n";
    for ($i = 1; $i <= $limite; $i++) {
        if (esPerfecto($i)) {
            echo "$i es un número perfecto\n";
        }
    }
}

// Solicitar al usuario que ingrese el límite
echo "Ingrese el límite hasta el cual desea encontrar números perfectos: ";
$limite = intval(fgets(STDIN));

mostrarNumerosPerfectos($limite);
?>