Summary:	show network activity using keyboard leds
Summary(pl):	pokazuje aktywno¶æ sieci u¿ywaj±c diod na klawiaturze
Name:		tleds
Version:	1.05b
Release:	2
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(pl):	Sieciowe/Narzêdzia
License:	GPL
Source0:	http://www.hut.fi/~jlohikos/public/%{name}-%{version}eta10.tgz
Patch0:		%{name}-activity.patch
URL:		http://www.iki.fi/Jouni.Lohikoski/tleds.html
BuildPrereq:	XFree86-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
ExclusiveArch:	%{ix86}

%description
tleds is a program which blinks keyboard LEDs (Light Emitting Diode)
indicating outgoing and incoming network packets on selected network
interface.

%description -l pl
tleds jest programem który zmienia stan diod na klawiaturze, pokazuj±c
obecno¶æ wychodz±cych oraz przychodz±cych pakietów na wybranym
interfejsie sieciowym.

%package -n xtleds
Summary:	show network activity using keyboard leds (XFree86 version)
Summary(pl):	pokazuje aktywno¶æ sieci u¿ywaj±c diod na klawiaturze (wersja dla XFree86)
Group:		X11/Applications
Group(de):	X11/Applikationen
Group(pl):	X11/Aplikacje
Requires:	%{name}
Requires:	XFree86-libs

%description -n xtleds
xtleds is a program which blinks keyboard LEDs (Light Emitting Diode)
indicating outgoing and incoming network packets on selected network
interface.

%description -n xtleds -l pl
xtleds jest programem który zmienia stan diod na klawiaturze,
pokazuj±c obecno¶æ wychodz±cych oraz przychodz±cych pakietów na
wybranym interfejsie sieciowym.

%prep
%setup  -q
%patch0 -p1

%build
%{__make} GCCOPTS="%{rpmcflags} %{rpmldflags} -DKERNEL2_1"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_prefix}/X11R6/bin} \
	$RPM_BUILD_ROOT%{_mandir}/man1

install tleds $RPM_BUILD_ROOT%{_bindir}
install xtleds $RPM_BUILD_ROOT%{_prefix}/X11R6/bin
install tleds.1 $RPM_BUILD_ROOT%{_mandir}/man1

install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/interfaces/up.d/ppp
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/interfaces/down.d/ppp

cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/interfaces/up.d/ppp/tleds
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

cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/interfaces/down.d/ppp/tleds
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

gzip -9nf README Changes

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/tleds
%attr(755,root,root) %{_sysconfdir}/sysconfig/interfaces/down.d/ppp/tleds
%attr(755,root,root) %{_sysconfdir}/sysconfig/interfaces/up.d/ppp/tleds
%{_mandir}/man*/*
%doc *.gz

%files -n xtleds
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/X11R6/bin/xtleds
