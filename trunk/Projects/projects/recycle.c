//
// Command-line utility to send a file or directory to the Recycle Bin
//
// This program only looks at the first command-line argument.  
// That argument must be a full path to the file.
//

#include <windows.h>
#include <string.h>

int main( int argc, char *argv[] )
{
	char filename[2048] = {0};
    SHFILEOPSTRUCT sfo = {0};

    if ( !argc ) return( 0 );
    if ( strlen(argv[0]) > 2048 ) return( 0 );

	sfo.hwnd = NULL;
	sfo.wFunc = FO_DELETE;
	sfo.pFrom = filename;
	sfo.fFlags = FOF_SILENT | FOF_NOCONFIRMATION | FOF_NOERRORUI | 
                 FOF_ALLOWUNDO | FOF_NOCONFIRMMKDIR;

    strcpy( filename, argv[0] );
    strcpy( filename + strlen(argv[0]), "\0\0" );

	return( SHFileOperation(&sfo) );
}
