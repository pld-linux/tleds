Summary:	show network activity using keyboard leds
Summary(pl):	pokazuje aktywno¶æ sieci u¿ywaj±c diod na klawiaturze
Name:		tleds
Version:	1.05b
Release:	1
Group:		Networking/Utilities
License:	GPL
Source0:	http://www.hut.fi/~jlohikos/public/%{name}-1.05beta10.tgz
Patch0:		%{name}-activity.patch
URL:		http://www.iki.fi/Jouni.Lohikoski/tleds.html
BuildPrereq:	XFree86-devel
BuildRoot:   	%{tmpdir}/%{name}-%{version}-%(id -u -n)
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
Summary(pl):	pokazuje aktywno¶æ sieci u¿ywaj±c diod na klawiaturze. Wersja dla XFree86.
Group:		X11/Utilities
Requires:	%{name}
Requires:	XFree86-libs

%description -n xtleds
xtleds is a program which blinks keyboard LEDs (Light Emitting Diode)
indicating outgoing and incoming network packets on selected network
interface.
				
%description -n xtleds -l pl
xtleds jest programem który zmienia stan diod na klawiaturze, pokazuj±c
obecno¶æ wychodz±cych oraz przychodz±cych pakietów na wybranym
interfejsie sieciowym.

%prep
%setup  -q
#%patch0 -p1

%build
make GCCOPTS="$RPM_OPT_FLAGS -s -DKERNEL2_1"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_prefix}/X11R6/bin} \
	$RPM_BUILD_ROOT%{_mandir}/man1

install tleds $RPM_BUILD_ROOT%{_bindir}
install xtleds $RPM_BUILD_ROOT%{_prefix}/X11R6/bin
install -m 644 tleds.1 $RPM_BUILD_ROOT%{_mandir}/man1

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	README Changes

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/tleds
%{_mandir}/man*/*
%doc *.gz

%files -n xtleds
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/X11R6/bin/xtleds

%changelog
