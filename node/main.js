var fs      = require('fs');
var pathObj = require('path');
var crypto  = require('crypto');
var builder = require('xmlbuilder'); // Install First: npm install xmlbuilder

var start = new Date().getTime();

/**
 * Return an Object sorted by it's Key
 */
var sortObjectByKey = function( obj ){
    var keys = [];
    var sorted_obj = {};

    for(var key in obj){
        if(obj.hasOwnProperty(key)){
            keys.push(key);
        }
    }

    // sort keys
    keys.sort();

    // create new array based on Sorted Keys
	for(mykey in keys)
		sorted_obj[mykey] = obj[mykey];

    return sorted_obj;
};
/**
 * PHP Like in Array
 **/
function in_array(needle, haystack) {

    var length = haystack.length;
    for(var i = 0; i < length; i++) {
        if(haystack[i] == needle)
			return true;
    }
    return false;

} // end of in_array()

function filesize( filename ) {

	var stats = fs.statSync(filename);
	return stats['size'];

}


// Main "Class"
var getDuplicates = {

	ext: false,
	path:false,
	files:{},

	// setPath( path )
	setPath: function( path ) 
	{

		this.path = this.parsePath( path );

		return this;

	},

	// setExt( ext )	
	setExt: function( ext )
	{
		this.ext = ext;

		return this;

	},

	// Parse Path
	// Remove last DIRECTORY_SEPARATOR from path
	parsePath: function( path ) {

		if( path.substr( path.length-1 ) == "\\" || path.substr( path.length - 1 ) == "/")
			path = path.substr( 0, path.length - 1 )
		return path;

	},

	// Get Files
	getFiles: function( path )
	{

		if( !path )
			path = this.path;

		var files = fs.readdirSync( path );
		for(var file in files){
			if ( !files.hasOwnProperty(file) ) continue;
			var filename = path + pathObj.sep + files[file];
			is_dir = false;
			try {
				is_dir = fs.statSync(filename).isDirectory();
			}
			catch(e) {
				console.log('Error in ' + filename);
			}
			if(is_dir)
			{
				this.getFiles(filename);
			}
			else
			{
				/**
				 * Get Extension
				 **/
				if( this.ext )
				{
					ext = filename.split('.');
					ext = ext[ext.length-1];
					if( !in_array(ext, this.ext))
						continue;
				}
			
				// checksum file
				var file_content = '';
				file_content = fs.readFileSync( filename ).toString();
				var hash     = crypto.createHash('md5');
				hash.setEncoding('hex');
				hash.update(file_content);
				hash.end();
				this.files[filename] = hash.read();
			}

		}
		if ( path == this.path )
		{
			this.filterFiles();
			return this;
		}

	}, // end of getFiles

	// Filter Files
	filterFiles: function()
	{

		var hash_list = {};
		var file_list = {};

		for( hash in this.files)
		{
			var current_hash = this.files[hash];
			if(hash_list.hasOwnProperty(current_hash))
				hash_list[current_hash] += 1;
			else
				hash_list[current_hash] = 1;
		}

		// Ordering the hash_list obje
		var keys = new Array();
		var new_hash_list = {};

		it = 0;
		for( key in hash_list )
		{
			keys[it] = key;
			it++;
		}
		keys.sort();

		for( key in keys )
			new_hash_list[keys[key]] = hash_list[keys[key]];

		// Removing files that have no duplicate and grouping them
		var new_files = {}
		for( file in this.files)
		{
			var hash = this.files[file];
			if( new_hash_list[ hash ] > 1 )
			{
				if( !new_files.hasOwnProperty( hash ) )
					new_files[hash] = new Array();
				new_files[hash].push( file );
			}
		}

		// Write in parent parameter
		this.files = new_files;
		return this;

	},

	// Write XML
	writeXML: function (xml_file )
	{

		var xml = builder.create('list');
		for( file in this.files )
		{
			var group = this.files[file];
			xml.ele('group');

			// Get Just First Item Filesize, duplicates should be the same having the same checksum
			size = filesize( group[0] );
			for( duplicate_file in group )
			{
				xml.ele('file',{'filesize': size}, group[duplicate_file]);
			}
		}
		var xmlString = xml.end({ pretty: true});
		fs.writeFileSync( xml_file, xmlString );

	}
};


var path = false;
var ext  = false;
var xml  = 'duplicates.xml';

var arg = process.argv;
// Setting Path
if( arg[2] != undefined)
	path = arg[2]
// Setting Extensions
if( arg[3] != undefined)
	ext = arg[3].split(',');

// Setting XML Filename
if( arg[4] != undefined)
	xml = arg[4]

if( path === false || path == '?' || path == 'help')
{
	console.log('==============================================================');
	console.log('Usage:');
	console.log('     node main.js [path] *[ext] *[xml_filename]');
	console.log('* - optional');
	console.log('');
	console.log('Example: node main.js C:\\ jpg,png duplicate_files.xml');
	console.log('==============================================================');

	return false;
}

getDuplicates.setPath( path );
if( ext )
	getDuplicates.setExt( ext );
getDuplicates.getFiles()
getDuplicates.writeXML(xml);

var end = new Date().getTime();
diff = (end - start) / 1000;
diff = Math.round(diff * 100) / 100;
console.log('Finished in ' + diff + ' seconds.');