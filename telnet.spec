Summary: telnet
Name: telnet
Group: test/test
Version: 0.0.0.1
Release: 1
License: GPL
ExclusiveArch: %{ix86}
Buildroot: %{_tmppath}/%{name}-root

%description
test

%prep
cat > conftest.c <<EOF
#include <unistd.h>
#include <stdio.h>
#include <signal.h>
volatile int count=0;
void handle(int foo) { count++; }
int main() {
    int pid=getpid();
    int tcount;
    signal(SIGINT, handle);
    kill(pid,SIGINT);
    kill(pid,SIGINT);
    kill(pid,SIGINT);
    tcount = count;
    if (tcount!=3) {
        fprintf(stderr, "count = %d\n", tcount);
        sleep(1);
        if(count != 3) {
	        fprintf(stderr, "count = %d\n", count);
		return 1;
	}
    }
    return 0;
} 
EOF


%build
gcc $RPM_OPT_FLAGS -g -o conftest conftest.c

%install
./conftest || exit 10

%clean
rm -rf ${RPM_BUILD_ROOT}

%files

%changelog
* Tue Jun 29 2004 Harald Hoyer <harald@redhat.com> - 1-1
- test script for strange signal behaviour

