%define	_snapshot	-pre20000412

Summary: The client program for the telnet remote login protocol.
Name: telnet
Version: 0.17
Release: 10
Copyright: BSD
Group: Applications/Internet
Source0: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit-devel/netkit-telnet-%{version}%{_snapshot}.tar.gz
Source2: telnet-client.tar.gz
Source3: telnet-xinetd
Patch4: telnet-0.10-escapechar.patch
Patch6: telnet-0.17-env.patch
Buildroot: %{_tmppath}/%{name}-root

%description
Telnet is a popular protocol for logging into remote systems over the
Internet.  The telnet package provides a command line telnet client.

Install the telnet package if you want to telnet to remote machines.

%package server
Requires: xinetd
Group: System Environment/Daemons
Summary: The server program for the telnet remote login protocol.

%description server
Telnet is a popular protocol for logging into remote systems over the
Internet.  The telnet-server package  a telnet daemon, which will
support remote logins into the host machine.  The telnet daemon is
enabled by default.  You may disable the telnet daemon by editing
/etc/xinet.d/telnet

Install the telnet-server package if you want to support remote logins
to your own machine.

%prep
%setup -q -n netkit-telnet-%{version}%{_snapshot}

mv telnet telnet-NETKIT
%setup -T -D -q -a 2 -n netkit-telnet-%{version}%{_snapshot}
%patch4 -p1 -b .escapechar

%patch6 -p1 -b .env

%build
sh configure
perl -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS),;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG

# XXX hack around gcc-2.96 problem
%ifarch i386
export RPM_OPT_FLAGS="`echo $RPM_OPT_FLAGS | sed -e s/-O2/-O0/`"
%endif

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

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%config(missingok) /etc/X11/applnk/Internet/telnet.desktop
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
