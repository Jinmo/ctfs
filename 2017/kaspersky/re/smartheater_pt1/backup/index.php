<?php

define("MAGIC_NUMBER"    ,    0);
define("ACTION"          ,    4);
define("PAYLOAD"         ,    5);
define("ACTION_GET"      , 0x01);
define("ACTION_SET"      , 0x02);
define("ACTION_RESET"    , 0x03);

function makePacket($act, $payload){

    $header = array();
    $header = array_fill(0, 5, 0x00);
    $header[MAGIC_NUMBER]   = 0xFE;
    $header[MAGIC_NUMBER+1] = 0xFF;
    $header[MAGIC_NUMBER+2] = 0xFE;
    $header[MAGIC_NUMBER+3] = 0xFF;
    $header[ACTION]         = $act;
    $header[PAYLOAD]        = $payload;
     
    return $header;
}

function send_recv($sendPacket){
    $rcv_msg = "";
    $timeout = 10;
    $socket = stream_socket_client('unix:///tmp/smart_heater.sock', $errorno, $errorstr, $timeout);
    stream_set_timeout($socket, $timeout);
    if (!$socket) {
        return array("ERROR", "Server does not respond. Try again later");
    }
    if(!fwrite($socket, $sendPacket)) {
        return array("ERROR", "Server does not respond. Try again later");
    }
    if (!($rcv_msg = fread($socket, 1024))) {
        return array("ERROR","Server does not respond. Try again later");
    } else { 
            return array("OK", $rcv_msg);
    }
}

function getUserIP()
{
  $ip = "";
 
  if (isset($_SERVER))
  {
    if (isset($_SERVER["HTTP_CLIENT_IP"])) {
      $ip = $_SERVER["HTTP_CLIENT_IP"];
    } else {
      $ip = $_SERVER["REMOTE_ADDR"];
    }
  }
  else {
    if ( getenv( 'HTTP_CLIENT_IP' ) ) {
      $ip = getenv( 'HTTP_CLIENT_IP' );
    } else {
      $ip = getenv( 'REMOTE_ADDR' );
    }
  }
  return $ip;
}

function temperature_control()
{
    if($_SERVER['REQUEST_METHOD'] != "GET" && $_SERVER['REQUEST_METHOD'] != "PUT") {
        header("HTTP/1.1 405 Method Not Allowed");
        return;
    }
    $local = '127.0.0.1';
    $user_ip = getUserIP();
    if(isset($user_ip) && $user_ip == $local) {
        if($_SERVER['REQUEST_METHOD'] == "GET") {
                $packet = makePacket(ACTION_GET, 0xFF);
                $sendPacket = "";
                for($i=0; $i<count($packet); $i++){
                    $sendPacket .= pack('C', $packet[$i]);
                }
                $result = send_recv($sendPacket);
                if($result){
                    header("Content-type: application/json");
                    echo json_encode($result);
                } 
        
        } else if($_SERVER['REQUEST_METHOD'] == "PUT") {
            $put_data = json_decode(file_get_contents("php://input"));
            if($put_data != null) {
                foreach ($put_data as $name => $value)
                {
                    switch ($name)
                    {
                        case 'Set':
                            {
                                if($value == null || !preg_match("/^-?[0-9]+$/", $value)) {
                                    header("HTTP/1.1 400 Bad Request");
                                    return;
                                } elseif ((int)$value <= 0) {
                                    header("Content-type: application/json");
                                    echo json_encode(["ERROR" => "Limiting temperature from 1°C to 30°C",]);
                                    return;
                                }
                                $packet = makePacket(ACTION_SET, (int)$value );
                                $sendPacket = "";
                                for($i=0; $i<count($packet); $i++){
                                    $sendPacket .= pack('c', $packet[$i]);
                                }
                                $result = send_recv($sendPacket);
                                if($result){
                                    header("Content-type: application/json");
                                    echo json_encode($result);
                                }
                            }    
                            break;

                        case 'Reset':
                            {
                                if($value == null || !preg_match("/^-?[0-9]+$/", $value)) {
                                    header("HTTP/1.1 400 Bad Request");
                                    return;
                                } elseif ((int)$value <= 0) {
                                    header("Content-type: application/json");
                                    echo json_encode(["ERROR" => "Limiting temperature from from 1°C to 30°C",]);
                                    return;
                                }
                                $packet = makePacket(ACTION_RESET, (int)$value );
                                $sendPacket = "";
                                for($i=0; $i<count($packet); $i++){
                                    $sendPacket .= pack('c', $packet[$i]);
                                }
                                $result = send_recv($sendPacket);
                                if($result){
                                    header("Content-type: application/json");
                                    echo json_encode($result);
                                }
                            }
                            break;

                        default:
                            {
                                header("HTTP/1.1 400 Bad Request");
                                return;
                            }
                            break;
                    }
                }
            } else {
                header("HTTP/1.1 400 Bad Request");
                return;
            }
            
        
        }
    } elseif(isset($user_ip) && $user_ip != $local) {
        header("HTTP/1.1 400 Bad Request");
        return;
    }
}

switch (@$_REQUEST['msubmenu'])
{
    case 'control': 
        {
            $funcName = 'temperature_' . $_REQUEST['msubmenu'];
            $funcName();
        }
        break;
    default:
        header("HTTP/1.1 501 Not Implemented");
        break;
}
?>
