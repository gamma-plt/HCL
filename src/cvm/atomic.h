extern bool debugging;

enum {INTEGER, CHAR, BOOLEAN};

vmint* atomic_abs(dct* args) {
	vmint* arg1 = args.get("arg1");

	return (vmintcmp(arg1, vmint(0))) ? vmintsub(arg1, vmint(0)) arg1: 
}