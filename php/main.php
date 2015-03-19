<?php
error_reporting(-1);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
ini_set('max_execution_time','0');

$start = microtime(true);

class getDuplicates {


    private $path       = false;
    private $extensions = array();
    public $files       = array();


    /**
     * Set Path
     **/
    public function setPath($path)
    {

        $this->path = $path;

        return $this;

    } // end of setPath()


    /**
     * Set Extensions
     **/
    public function setExtensions( $ext )
    {

        $this->extensions = $ext;
        
        return $this;

    } // end of setExtensions()


    /**
     * Main Method
     **/
    public function getFiles( $path = false )
    {

        // Set the path on the first initialization
        $first_instance = false;
        if( !$path )
        {
            $path = $this->path;
            $first_instance = true;
        }

        // Loop throw files
        $files = @scandir( $path );
        if( !$files )
            return array();
        foreach( $files as $file )
        {
            if( !in_array( $file, array('.','..') ) )
            {
                $current_file = $path . DIRECTORY_SEPARATOR . $file;
                if( is_dir( $current_file ) )
                {
                    $this->getFiles( $current_file );
                }
                else
                {
                    // Verify extensions
                    if( !empty( $this->extensions ) )
                    {
                        if( !in_array( strtolower( substr($current_file,-3) ), $this->extensions ) )
                            continue;
                    }
                    // Get Filesize
                    $filesize = md5_file( $current_file );
                    if( $filesize )
                        $this->files[$current_file] = $filesize;
                }
            } // end of exclude base and up dir
        } // end of loop

        // Remove files that are not duplicates
        if( $first_instance )
            $this->filterFiles();

        return $this;

    } // end of getFiles()

    /**
     * Eliminate Duplicates
     **/
    public function filterFiles()
    {

        $total = count( $this->files );
        $temp = array_count_values( $this->files );
        asort( $temp );
        foreach($temp as $hash => $count)
        {
            // Stop looping for duplicates
            if( $count > 1)
                break;
            if( ( $key = array_search($hash, $this->files) ) !== false )
                unset($this->files[$key]);
        }

        $hash = array_count_values( $this->files );
        foreach( $hash as $key => $val)
            $hash[$key] = array();

        foreach( $this->files as $file => $hash_value)
            $hash[$hash_value][] = $file;

        $this->files = array_values( $hash );

    } // end of filterFiles()


    /**
     * Write XML
     **/
    public function writeXML( $xml_filename )
    {

        $xml = new DOMDocument();
        $list = $xml->createElement("list");
        foreach( $this->files as $group)
        {
            $group_xml = $xml->createElement("group");
            foreach( $group as $file )
            {
                $file_node =  $xml->createElement("file", $file);

                // Get File Size
                $filesize_xml = $xml->createAttribute('filesize');
                $filesize = @filesize($file);
                if($filesize)
                    $filesize_xml->value = $filesize;
                else
                    $filesize_xml->value = 0;
                $file_node->appendChild($filesize_xml);
                $group_xml->appendChild($file_node);
            }
            $list->appendChild($group_xml);
        }
        $xml->appendChild($list);

        $xml->save( $xml_filename );

    } // end of writeXML


} // end of class


$path = false;
$ext  = false;
$xml  = 'duplicates.xml';


$path = isset($argv[1]) ? $argv[1] : false;
$ext  = isset($argv[2]) ? explode(',',$argv[2]) : false;
$xml  = isset($argv[3]) ? $argv[3] : $xml;

if(!$path || in_array($path, array('?','help') ) )
{
	echo '==============================================================' . "\n";
	echo 'Usage:' . "\n";
	echo '     main.php [path] *[ext] *[xml_filename]' . "\n";
	echo '* - optional';
	echo "\n\n";
	echo 'Example: main.php C:\\ jpg,png duplicate_files.xml' . "\n";
	echo '==============================================================' . "\n";
    exit();
}


$scan = new getDuplicates();
$scan->setPath( $path );
$scan->setExtensions( $ext );
$scan->getFiles();
$scan->writeXml( $xml);

//var_dump( $scan->files);

$diff = microtime(true) - $start;
$diff = number_format($diff, 2, ',','.');

echo '<strong>Finished in ' . $diff . ' seconds.</strong>';
?>
