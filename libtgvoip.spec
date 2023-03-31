%define major	2
%define libname	%mklibname tgvoip %{version}
%define devname	%mklibname -d tgvoip
%global commit0 0c0a6e476df58ee441490da72ca7a32f83e68dbd
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20200521

Summary: VoIP library for Telegram clients
Name: libtgvoip
Version: 2.4.4
Release: 3

# Libtgvoip shared library - Public Domain.
# Bundled webrtc library - BSD with patented echo cancellation algorithms.
License: Public Domain and BSD

URL: https://github.com/telegramdesktop/%{name}
Summary: VoIP library for Telegram clients
Source0: %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
Patch1: libtgvoip-system-json11.patch

Provides: bundled(webrtc-audio-processing) = 0.3
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(json11)
BuildRequires: alsa-oss-devel
BuildRequires: pkgconfig(alsa)
BuildRequires: opus-devel
BuildRequires: gyp >= 0.1-0.25.0
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: python3-pkg-resources

%description
Provides VoIP library for Telegram clients.

%package -n	%{libname}
Summary:	VoIP library for Telegram clients
Group:		System/Libraries

%description -n	%{libname}
VoIP library for Telegram clients


%package -n %{devname}
Summary: Development files for %{name}
Requires: %{libname} = %{EVRD}
Provides: tgvoip-devel = %{EVRD}

%description -n %{devname}
%{summary}.

%prep
%autosetup -n %{name}-%{commit0} -p1
rm -f json11.*

%build
#export CC=gcc
#export CXX=g++
export OBJCXX="%{__cxx}"
autoreconf --force --install
%configure --disable-static
%make_build

%install
%make_install

mkdir -p "%{buildroot}%{_libdir}/pkgconfig"

cat <<EOF >tgvoip.pc
includedir=%_includedir

Name: tgvoip
Description: %summary
URL: %url
Version: %version
Requires: opus
Conflicts:
Libs: -ltgvoip
Libs.private: -ldl -lpthread -lopus -lcrypto
Cflags: -I\${includedir}/tgvoip
EOF

install -m 0644 tgvoip.pc %{buildroot}%{_libdir}/pkgconfig

%files -n %{libname}
%{_libdir}/%{name}.so.*

%files -n %{devname}
%{_includedir}/tgvoip
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/*.pc
