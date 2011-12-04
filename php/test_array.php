<?php

$arr = array(
    array('name' => 'wo',
          'age' =>  'ni'),
    array('name' => 'w11',
          'age' =>  'n11'),
);
array_walk($arr, 'cleanData');

?>
