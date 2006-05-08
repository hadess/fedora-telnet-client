Summary: The client program for the telnet remote login protocol.
Name: telnet
Version: 0.17
Release: 36
Epoch: 1
License: BSD
Group: Applications/Internet
Source0: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-telnet-%{version}.tar.gz
Source2: telnet-client.tar.gz
Source3: telnet-xinetd
Source4: telnet.wmconfig
Patch1: telnet-client-cvs.patch
Patch5: telnetd-0.17.diff
Patch6: telnet-0.17-env.patch
Patch7: telnet-0.17-issue.patch
Patch8: telnet-0.17-sa-01-49.patch
Patch9: telnet-0.17-env-5x.patch
Patch10: telnet-0.17-pek.patch
Patch11: telnet-0.17-8bit.patch
Patch12: telnet-0.17-argv.patch
Patch13: telnet-0.17-conf.patch
Patch14: telnet-0.17-cleanup_race.patch
Patch15: telnetd-0.17-pty_read.patch
Patch16: telnet-0.17-CAN-2005-468_469.patch
Patch17: telnet-0.17-linemode.patch
Patch18: telnet-gethostbyname.patch

BuildPreReq: ncurses-devel
Buildroot: %{_tmppath}/%{name}-root

%description
Telnet is a popular protocol for logging into remote systems over the
Internet. The telnet package provides a command line telnet client.

%package server
Requires: xinetd
Group: System Environment/Daemons
Summary: The server program for the telnet remote login protocol.

%description server
Telnet is a popular protocol for logging into remote systems over the
Internet. The telnet-server package includes a telnet daemon that
supports remote logins into the host machine. The telnet daemon is
disabled by default. You may enable the telnet daemon by editing
/etc/xinetd.d/telnet.

%prep
%setup -q -n netkit-telnet-%{version}

mv telnet telnet-NETKIT
%setup -T -D -q -a 2 -n netkit-telnet-%{version}

%patch1 -p0 -b .cvs
%patch5 -p0 -b .fix
%patch6 -p1 -b .env
%patch10 -p0 -b .pek
%patch7 -p1 -b .issue
%patch8 -p1 -b .sa-01-49
%patch11 -p1 -b .8bit
%patch12 -p1 -b .argv
%patch13 -p1 -b .confverb
%patch14 -p1 -b .cleanup_race 
%patch15 -p0 -b .pty_read
%patch16 -p1 -b .CAN-2005-468_469
#%patch17 -p1 -b .linemode
%patch18 -p1 -b .gethost

%build
export OPT_FLAGS="$RPM_OPT_FLAGS -g"
export LD_FLAGS="$OPT_FLAGS"
export CC_FLAGS="$CC_FLAGS"
if echo 'int main () { return 0; }' | gcc -pie -fPIE -O2 -xc - -o pietest 2>/dev/null; then
        if ./pietest; then
%ifarch s390 s390x ia64
		 export CC_FLAGS="$OPT_FLAGS -fPIE"
%else
		 export CC_FLAGS="$OPT_FLAGS -fpie"
%endif
		 export LD_FLAGS="$OPT_FLAGS -pie"
	fi
        rm -f pietest
fi

sh configure --with-c-compiler=gcc 
perl -pi -e '
    s,-O2,\$(CC_FLAGS),;
    s,LDFLAGS=.*,LDFLAGS=\$(LD_FLAGS),;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG

# remove stripping
perl -pi -e 's|install[ ]+-s|install|g' \
	./telnet/GNUmakefile \
	./telnetd/Makefile \
	./telnetlogin/Makefile \
	./telnet-NETKIT/Makefile

make

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man5
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8

make INSTALLROOT=${RPM_BUILD_ROOT} install

mkdir -p ${RPM_BUILD_ROOT}/etc/xinetd.d
install -m644 %SOURCE3 ${RPM_BUILD_ROOT}/etc/xinetd.d/telnet

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%{_bindir}/telnet
%{_mandir}/man1/telnet.1*

%files server
%defattr(-,root,root)
%config(noreplace) /etc/xinetd.d/telnet
%{_sbindir}/in.telnetd
%{_mandir}/man5/issue.net.5*
%{_mandir}/man8/in.telnetd.8*
%{_mandir}/man8/telnetd.8*

%changelog
* Mon May 08 2006 Harald Hoyer <harald@redhat.com> - 1:0.17-36
- patch to remove gethostbyname() (bug #190296)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:0.17-35.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:0.17-35.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Mar 17 2005 Harald Hoyer <harald@redhat.com> - 1:0.17-35
- fixed CAN-2005-468 and CAN-2005-469

* Wed Mar 02 2005 Harald Hoyer <harald@redhat.com> 
- rebuilt

* Fri Jan 21 2005 Harald Hoyer <harald@redhat.com> - 1:0.17-33
- added patch telnetd-0.17-pty_read.patch, which fixes 145636

* Thu Jan 13 2005 Jason Vas Dias <jvdias@redhat.com> - 1:0.17-31
- bug 143929 / 145004 : fix race condition in telnetd on wtmp lock 
- when cleanup() is entered from main process and in signal
- handler 

* Mon Jun 28 2004 Harald Hoyer <harald@redhat.com> - 1:0.17-30
- fixed 126858: Too long /proc/X/cmdline: bad ps output when 
                piped to less/more

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb  5 2004 Harald Hoyer <harald@redhat.com> - 1:0.17-27
- added PIE compile flags

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 28 2003 Harald Hoyer <harald@redhat.de> 1:0.17-26
- cleanup of spec file
- 8bit binary patch #91023

* Wed Jan 29 2003 Harald Hoyer <harald@redhat.de> 0.17-25
- rebuilt 

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 11 2002 Harald Hoyer <harald@redhat.de> 0.17-24
- changed description
- removed unused .desktop files

* Tue Jul 23 2002 Harald Hoyer <harald@redhat.de> 0.17-23
- removed prestripping

* Tue Jul  9 2002 Harald Hoyer <harald@redhat.de>
- removed x86 -O gcc-2.96 hack (#59514)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun  6 2002 Tim Powers <timp@redhat.com>
- bump release number and rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Sep 06 2001 Harald Hoyer <harald@redhat.de> 0.17-20
- hopefully fixed #52817, #52224

* Thu Aug 16 2001 Bill Nottingham <notting@redhat.com>
- bump version for 7.2

* Wed Aug 15 2001 Bill Nottingham <notting@redhat.com>
- fix versioning

* Tue Jul 31 2001 Harald Hoyer <harald@redhat.de>
- fixed security issues (#50335)
- patched the patches to fit the 5x version
- one world -> one spec file for all versions ;)

* Sat Jul 21 2001 Tim Powers <timp@redhat.com>
- no applnk file, it's clutrtering the menus

* Wed Jul 17 2001 Bill Nottingham <notting@redhat.com>
- apply the patch, duh (and fix it while we're here)

* Tue Jul 10 2001 Bill Nottingham <notting@redhat.com>
- make /etc/issue.net parsing match the various gettys

* Mon Jun 18 2001 Harald Hoyer <harald@redhat.de>
- merged Jakubs and Pekka's patches 

* Wed Apr  4 2001 Jakub Jelinek <jakub@redhat.com>
- don't let configure to guess compiler, it can pick up egcs

* Fri Mar  9 2001 Pekka Savola <pekkas@netcore.fi>
- update to 0.17
- apply latest changes from CVS to telnet client, enable IPv6
- BuildPreReq ncurses-devel

* Mon Jan 22 2001 Helge Deller <hdeller@redhat.com>
- added swedish & german translation to .desktop-file (#15332)

* Sat Dec 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- mark the xinetd config file as config(noreplace)

* Fri Dec 01 2000 Trond Eivind Glomsrød <teg@redhat.com>
- make sure the server is turned off by default

* Tue Jul 18 2000 Bill Nottingham <notting@redhat.com>
- add description & default to xinetd file

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- update to 0.17-pre20000412.

* Tue May 23 2000 Trond Eivind Glomsrød <teg@redhat.com>
- moved the xinet entry to the server

* Mon May 22 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add an entry to /etc/xinetd.d

* Tue May 16 2000 Jeff Johnson <jbj@redhat.com>
- permit telnet queries only for exported variables.

* Fri Mar 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.17

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Fri Feb 11 2000 Bill Nottingham <notting@redhat.com>
- fix description

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- wmconfig gone

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- fix description

* Tue Jan  4 2000 Bill Nottingham <notting@redhat.com>
- split client and server

* Tue Dec 21 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.16.

* Sun Oct 10 1999 Matt Wilson <msw@redhat.com>
- corrected the Terminal setting of the .desktop (needs to be 'true' not '1')

* Sat Sep 24 1999 Preston Brown <pbrown@redhat.com>
- red hat .desktop entry

* Sat Aug 21 1999 Jeff Johnson <jbj@redhat.com>
- rebuild for 6.1.

* Wed Aug 18 1999 Bill Nottingham <notting@redhat.com>
- don't trust random TERM variables in telnetd (#4560)

* Wed Jun  2 1999 Jeff Johnson <jbj@redhat.com>
- fix (#3098).

* Thu May 27 1999 Antti Andreimann <Antti.Andreimann@mail.ee>
- fixed the problem with escape character (it could not be disabled)
- changed the spec file to use %setup macro for unpacking telnet-client

* Thu Apr 15 1999 Jeff Johnson <jbj@redhat.com>
- use glibc utmp routines.

* Thu Apr  8 1999 Jeff Johnson <jbj@redhat.com>
- fix the fix (wrong way memcpy).

* Wed Apr  7 1999 Jeff Johnson <jbj@redhat.com>
- fix "telnet localhost" bus error on sparc64 (alpha?).

* Tue Apr  6 1999 Jeff Johnson <jbj@redhat.com>
- use OpenBSD telnet client (and fix minor core dump with .telnetrc #247)

* Thu Mar 25 1999 Erik Troan <ewt@redhat.com>
- use openpty in telnetd

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 22)

* Mon Mar 15 1999 Jeff Johnson <jbj@redhat.com>
- compile for 6.0.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 24 1998 Cristian Gafton <gafton@redhat.com>
- compile C++ code using egcs

* Tue Apr 14 1998 Erik Troan <ewt@redhat.com>
- built against new ncurses

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- added wmconfig entry

* Tue Jul 15 1997 Erik Troan <ewt@redhat.com>
- initial build
