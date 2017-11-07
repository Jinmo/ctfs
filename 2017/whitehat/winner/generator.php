<?php
$init_seed = "what";
function generator()
{
    global $init_seed;
    $PATH = "./s3cre7_fi1e";
    if($init_seed === "what")
    {
        $init_seed = $seed = intval(uniqid(),10);
    }
    
    $init_seed = $seed = $init_seed;

    srand($init_seed);
    for( $i=0; $i<$init_seed%100; $i++)
    {
        $seed = rand() * rand();
        srand($seed);
        $tmp = rand()*rand();
        $length = strlen($tmp);
        $cutting = (int)($length/4);
        $tmp2= substr($seed,$cutting,$length-$cutting*2);
        $seed = $tmp2*$tmp2;
    }
    $ret = array(7);
    $new_seed = 0;
    for( $i=0; $i<7; $i++)
    {    $new_seed = rand();
        $number = ($new_seed%77)+1;
        if(in_array($number,$ret))
        {
            $i--;
            continue;
        }
        $ret[$i] = $number;
    }
    $init_seed = $new_seed;
    return $ret;
    
}

$found = 0;
for($i=0;;$i++){
    $r=generator();
    $luckyNumber=$r;
        sort($luckyNumber);
    $luckyNumber = implode(",",$luckyNumber);
    if($found) {
        echo $luckyNumber; echo "\n";
        exit;
    }
    if($luckyNumber == $argv[1])
        $found = 1;
}
?>
