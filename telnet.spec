%define telnet_version  0.17
%define telnet_release  23

%define telnet_errata_release  19

#
# define b5x for old 5.x release erratas
# define b6x for old 6.x release erratas
#
# define b6x 1
# define b5x 1

%{?b5x:%define old_5x  1}
%{!?b5x:%define old_5x  0}

%{?b6x:%define old_6x  1}
%{!?b6x:%define old_6x  0}

%if %{old_5x} && %{old_6x}
%{error: You cannot build for .5x and .6x at the same time}
%quit
%endif

%if %{old_5x}
%define b5x 1
%undefine b6x
%endif

%if %{old_6x}
%define b6x 1
%undefine b5x
%endif

%{?b5x:%define dist_prefix  0.5x}
%{?b6x:%define dist_prefix  0.6x}

Summary: The client program for the telnet remote login protocol.
Name: telnet
%{?dist_prefix:Version: %{telnet_version}%{dist_prefix}}
%{!?dist_prefix:Version: %{telnet_version}}
%{!?dist_prefix:Release: %{telnet_release}}
%{?dist_prefix:Release: %{telnet_errata_release}%{dist_prefix}}
Serial: 1
Copyright: BSD
Group: Applications/Internet
Source0: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-telnet-%{telnet_version}.tar.gz
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
BuildPreReq: ncurses-devel
Buildroot: %{_tmppath}/%{name}-root

%description
Telnet is a popular protocol for logging into remote systems over the
Internet. The telnet package provides a command line telnet client.

%if ! %{old_5x}
%package server
Requires: xinetd
Group: System Environment/Daemons
Summary: The server program for the telnet remote login protocol.

%description server
Telnet is a popular protocol for logging into remote systems over the
Internet. The telnet-server package includes a telnet daemon that
supports remote logins into the host machine. The telnet daemon is
enabled by default. You may disable the telnet daemon by editing
/etc/xinetd.d/telnet.

%endif
%prep
%setup -q -n netkit-telnet-%{telnet_version}

mv telnet telnet-NETKIT
%setup -T -D -q -a 2 -n netkit-telnet-%{telnet_version}

%if %{old_5x}
%patch5 -p0 -b .fix
%patch9 -p1 -b .env
%else
%patch1 -p0 -b .cvs
%patch5 -p0 -b .fix
%patch6 -p1 -b .env
%patch10 -p0 -b .pek
%endif
%patch7 -p1 -b .issue
%patch8 -p1 -b .sa-01-49
%build
sh configure --with-c-compiler=gcc
perl -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS),;
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

mkdir -p ${RPM_BUILD_ROOT}/etc/X11/applnk/Internet
cat > ${RPM_BUILD_ROOT}/etc/X11/applnk/Internet/telnet.desktop <<EOF
[Desktop Entry]
Name=Telnet
Type=Application
Comment=client to connect to remote machines via a text interface
Comment[de]=Telnet-Client für den textbasierten Remotezugang zu anderen Computern
Comment[sv]=klient för anslutning till fjärrmaskiner via ett textgränssnitt
Exec=telnet
Icon=telnet.xpm
Terminal=true
EOF

mkdir -p ${RPM_BUILD_ROOT}/etc/xinetd.d
install -m644 %SOURCE3 ${RPM_BUILD_ROOT}/etc/xinetd.d/telnet

mkdir -p $RPM_BUILD_ROOT/etc/X11/wmconfig
install -m644 $RPM_SOURCE_DIR/telnet.wmconfig $RPM_BUILD_ROOT/etc/X11/wmconfig/telnet

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%{_bindir}/telnet
%{_mandir}/man1/telnet.1*
%{?b5x:%config(missingok) /etc/X11/wmconfig/telnet}
%{?b6x:%config(missingok) /etc/X11/applnk/Internet/telnet.desktop}

%{!?b5x:%files server}
%defattr(-,root,root)
%{!?b5x:%config(noreplace) /etc/xinetd.d/telnet}
%{_sbindir}/in.telnetd
%{_mandir}/man5/issue.net.5*
%{_mandir}/man8/in.telnetd.8*
%{_mandir}/man8/telnetd.8*

%changelog
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
