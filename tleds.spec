Summary:	Show network activity using keyboard leds
Summary(pl.UTF-8):	Pokazywanie aktywności sieci przy użyciu diod na klawiaturze
Name:		tleds
Version:	1.05b
Release:	5
License:	GPL
Group:		Networking/Utilities
Source0:	http://www.hut.fi/~jlohikos/public/%{name}-%{version}eta10.tgz
# Source0-md5:	9372325d0383b7ea38e463dae1f1de78
Patch0:		%{name}-activity.patch
URL:		http://www.iki.fi/Jouni.Lohikoski/tleds.html
BuildRequires:	xorg-lib-libX11-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
tleds is a program which blinks keyboard LEDs (Light Emitting Diode)
indicating outgoing and incoming network packets on selected network
interface.

%description -l pl.UTF-8
tleds jest programem który zmienia stan diod na klawiaturze, pokazując
obecność wychodzących oraz przychodzących pakietów na wybranym
interfejsie sieciowym.

%package -n xtleds
Summary:	Show network activity using keyboard leds (X11 version)
Summary(pl.UTF-8):	Pokazywanie aktywności sieci przy użyciu diod na klawiaturze (wersja dla X11)
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description -n xtleds
xtleds is a program which blinks keyboard LEDs (Light Emitting Diode)
indicating outgoing and incoming network packets on selected network
interface.

%description -n xtleds -l pl.UTF-8
xtleds jest programem który zmienia stan diod na klawiaturze,
pokazując obecność wychodzących oraz przychodzących pakietów na
wybranym interfejsie sieciowym.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	GCCOPTS="%{rpmcflags} %{rpmldflags} -DKERNEL2_1"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_prefix}/X11R6/bin} \
	$RPM_BUILD_ROOT%{_mandir}/man1 \
	$RPM_BUILD_ROOT/etc/sysconfig/interfaces/{up,down}.d/ppp

install tleds $RPM_BUILD_ROOT%{_bindir}
install xtleds $RPM_BUILD_ROOT%{_bindir}
install tleds.1 $RPM_BUILD_ROOT%{_mandir}/man1
echo '.so tleds.1' >$RPM_BUILD_ROOT%{_mandir}/man1/xtleds.1

cat <<EOF >$RPM_BUILD_ROOT/etc/sysconfig/interfaces/up.d/ppp/tleds
#!/bin/sh
#this script will make your keyboard LEDs blink on (in|out)comming network packets
. /etc/rc.d/init.d/functions

if [ -f /var/lock/subsys/tleds ]; then
	msg_starting tleds
	daemon tleds -d 200 -c ppp0
	touch /var/lock/subsys/tleds
else
	msg_Already_Running tleds
fi
EOF

cat <<EOF >$RPM_BUILD_ROOT/etc/sysconfig/interfaces/down.d/ppp/tleds
#!/bin/sh
#this script will shut down tleds
. /etc/rc.d/init.d/functions

if [ -f /var/lock/subsys/tleds ]; then
	msg_stopping tleds
	killproc tleds
	rm -f /var/lock/subsys/tleds
else
	msg_Not_Running tleds
exit 1
fi
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README Changes
%attr(755,root,root) %{_bindir}/tleds
%attr(755,root,root) /etc/sysconfig/interfaces/down.d/ppp/tleds
%attr(755,root,root) /etc/sysconfig/interfaces/up.d/ppp/tleds
%{_mandir}/man1/tleds.1*

%files -n xtleds
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xtleds
%{_mandir}/man1/xtleds.1*
