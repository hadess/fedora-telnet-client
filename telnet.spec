%global _hardened_build 1

Summary: The client program for the Telnet remote login protocol
Name: telnet
Version: 0.17
Release: 82.client%{?dist}
Epoch: 1
License: BSD
Source0: https://src.fedoraproject.org/lookaside/pkgs/telnet/telnet-client.tar.gz/d74983062470c5a3e7ae14f34c489e00/telnet-client.tar.gz
Source1: MCONFIG
Patch1: telnet-client-cvs.patch
Patch6: telnet-0.17-env.patch
Patch10: telnet-0.17-pek.patch
Patch11: telnet-0.17-8bit.patch
Patch16: telnet-0.17-CAN-2005-468_469.patch
Patch18: telnet-gethostbyname.patch
Patch21: telnet-0.17-errno_test_sys_bsd.patch
Patch25: telnet-rh704604.patch
Patch27: telnet-0.17-force-ipv6-ipv4.patch
Patch28: netkit-telnet-0.17-core-dump.patch
Patch29: netkit-telnet-0.17-gcc7.patch
Patch30: netkit-telnet-0.17-manpage.patch
Patch31: netkit-telnet-0.17-telnetrc.patch

BuildRequires: ncurses-devel systemd gcc gcc-c++
BuildRequires: perl-interpreter

%description
Telnet is a popular protocol for logging into remote systems over the
Internet. The package provides a command line Telnet client

%prep
%setup -q -c telnet-client

%patch1 -p0 -b .cvs
%patch6 -p1 -b .env
%patch10 -p0 -b .pek
%patch11 -p1 -b .8bit
%patch16 -p1 -b .CAN-2005-468_469
%patch18 -p1 -b .gethost
%patch21 -p1 -b .errnosysbsd
%patch25 -p1 -b .rh704604
%patch27 -p1 -b .ipv6-support
%patch28 -p1 -b .core-dump
%patch29 -p1 -b .gcc7
%patch30 -p1 -b .manpage
%patch31 -p1 -b .telnetrc

%build
%ifarch s390 s390x
    export CC_FLAGS="$RPM_OPT_FLAGS -fPIE"
%else
    export CC_FLAGS="$RPM_OPT_FLAGS -fpie"
%endif

export LD_FLAGS="$RPM_LD_FLAGS -z now -pie"

# remove stripping
perl -pi -e 's|install[ ]+-s|install|g' \
    ./telnet/GNUmakefile
perl -pi -e 's|include ../MRULES||g' \
    ./telnet/GNUmakefile

cp %{SOURCE1} .
cd telnet/

make telnet

%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
cp -a telnet/telnet ${RPM_BUILD_ROOT}%{_bindir}

%files
%defattr(-,root,root,-)
%{_bindir}/telnet

%changelog
* Sat Dec 05 2020 Bastien Nocera <bnocera@redhat.com> - 0.17-82.client
+ telnet-0.17-82
- Client only package, based off Fedora telnet
  https://src.fedoraproject.org/rpms/telnet
