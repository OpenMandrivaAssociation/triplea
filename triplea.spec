%define	_version2	%(echo %version | tr . _)

Name:		triplea
Version:	1.6.1.1
Release:	1
Summary:	A networked open source strategy game
Group:		Games/Strategy
License:	GPLv2+
URL:		http://triplea.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}_%{_version2}_source_code_only.zip
Source1:	%{name}.png
Patch0:		%{name}-build.xml.patch

BuildRequires:	ant
BuildRequires:	dos2unix
BuildRequires:	jakarta-commons-codec
BuildRequires:	jakarta-commons-logging
BuildRequires:	java-devel
BuildRequires:	java-rpmbuild
BuildRequires:	jpackage-utils
BuildRequires:	junit
BuildRequires:	ant-junit
BuildRequires:	xerces-j2
BuildRequires:	xmlbeans
Requires:	jakarta-commons-codec
Requires:	jakarta-commons-logging
Requires:	java >= 1.6
BuildArch:	noarch

%description
Triplea is a networked open source strategy game, based on the 
Axis & Allies board game. It allows people to implement and play various 
strategy board games (i.e. Axis & Allies). The TripleA engine has full 
networking support for online play, support for sounds, XML support for 
game files, and has its own imaging subsystem that allows for customized
user editable maps to be used. TripleA is versatile, scalable and robust.


%prep
%setup -q -n %{name}_%{_version2}
%patch0 -p1 -b .orig~
rm triplea_mac_os_x.sh
rm triplea_windows.bat
dos2unix readme.html changelog.txt doc/*.html doc/*.css

%build
# ant doesn't make required folders in mdv2011 and earlier.
%if %mdkversion =< 201100
mkdir bin release
%endif
%ant zip

%install
# ant makes a zip file, so unzip that into the final dir.
# Don't know another way to do it, yet.
install -dm 755 %{buildroot}%{_gamesdatadir}
unzip -q -d %{buildroot}%{_gamesdatadir} release/%{name}_all_platforms.zip

# startscript
install -dm 755 %{buildroot}%{_gamesbindir}

cat > %{buildroot}%{_gamesbindir}/%{name} << EOF
#!/bin/sh
%{_gamesdatadir}/%{name}/%{name}_unix.sh
EOF
chmod 755 %{buildroot}%{_gamesbindir}/%{name}

# icon and menu-entry
install -dm 755 %{buildroot}%{_datadir}/pixmaps
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps

install -dm 755 %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Comment=Axis and Allies clone
Name=TripleA
GenericName=TripleA
Type=Application
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Categories=Game;StrategyGame;
Terminal=false
EOF

%files
%doc changelog.txt readme.html doc/*
%{_gamesbindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%dir %{_gamesdatadir}/%{name}
%{_gamesdatadir}/%{name}/*

