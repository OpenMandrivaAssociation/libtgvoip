%define major	2
%define libname	%mklibname tgvoip %{version}
%define devname	%mklibname -d tgvoip
%define date 20180529
%define alpha alpha4

Summary: VoIP library for Telegram clients
Name: libtgvoip
Version: 2.4.4
Release: 1

# Libtgvoip shared library - Public Domain.
# Bundled webrtc library - BSD with patented echo cancellation algorithms.
License: Public Domain and BSD
URL: https://github.com/grishka/%{name}

# git archive --format=tar --prefix libtgvoip-2.0-alpha4-$(date +%Y%m%d)/ HEAD | xz -vf > ../libtgvoip-2.0-alpha4-$(date +%Y%m%d).tar.xz
#Source0: %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
#Source0: libtgvoip-%{version}-%{alpha}-%{date}.tar.xz
Source0: https://github.com/grishka/libtgvoip/archive/%{version}.tar.gz
Patch0: %{name}-build-fixes.patch

Provides: bundled(webrtc-audio-processing) = 0.3
BuildRequires: pkgconfig(libpulse)
BuildRequires: alsa-oss-devel
BuildRequires: pkgconfig(alsa)
BuildRequires: openssl-devel
BuildRequires: opus-devel
BuildRequires: gyp >= 0.1-0.25.0
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: python2-pkg-resources
%ifarch x86_64
BuildRequires: c++-devel
%endif

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
%setup -n %{name}-%{version}
%apply_patches

%build
export VOIPVER="%{version}"
export SOVER=%{version}
export CXXFLAGS="%{optflags} -std=gnu++11 -ldl -lpthread -lopus -lssl -lcrypto"
%{__python2} %{_bindir}/gyp --format=cmake --depth=. --generator-output=. -Goutput_dir=out -Gconfig=Release %{name}.gyp

pushd out/Release
	%cmake -G Ninja
	%ninja_build
popd

%install
# Installing shared library...
mkdir -p "%{buildroot}%{_libdir}"
install -m 0755 -p out/Release/build/lib.target/%{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so.%{version}"
ln -s %{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so.%{major}"
ln -s %{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so"

# Installing additional development files...
mkdir -p "%{buildroot}%{_includedir}/%{name}"
find . -maxdepth 1 -type f -name "*.h" -exec install -m 0644 -p '{}' %{buildroot}%{_includedir}/%{name} \;
mkdir -p "%{buildroot}%{_includedir}/%{name}/audio"
find audio -maxdepth 1 -type f -name "*.h" -exec install -m 0644 -p '{}' %{buildroot}%{_includedir}/%{name}/audio \;
mkdir -p "%{buildroot}%{_includedir}/%{name}/video"
find video -maxdepth 1 -type f -name "*.h" -exec install -m 0644 -p '{}' %{buildroot}%{_includedir}/%{name}/video \;


%files -n %{libname}
%{_libdir}/%{name}.so.*

%files -n %{devname}
%{_includedir}/%{name}
%{_libdir}/%{name}.so
