%define major	1
%define libname	%mklibname tgvoip %{version}
%define devname	%mklibname -d tgvoip

Summary: VoIP library for Telegram clients
Name: libtgvoip
Version: 1.0.3
Release: 4

# Libtgvoip shared library - Public Domain.
# Bundled webrtc library - BSD with patented echo cancellation algorithms.
License: Public Domain and BSD
URL: https://github.com/grishka/%{name}

Source0: %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0: %{name}-build-fixes.patch

Provides: bundled(webrtc-audio-processing) = 0.3
BuildRequires: pkgconfig(libpulse)
BuildRequires: alsa-oss-devel
BuildRequires: openssl-devel
BuildRequires: opus-devel
BuildRequires: gyp >= 0.1-0.25.0
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: c++-devel

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
export CXXFLAGS="%{optflags} -stdlib=libc++ -lpthread -ldl -std=gnu++17"
export SOVER=%{version}
%{__python2} %{_bindir}/gyp --format=cmake --depth=. --generator-output=. -Goutput_dir=out -Gconfig=Release %{name}.gyp


pushd out/Release
	%cmake -G Ninja
	%ninja_build
popd

%install
# Installing shared library...
mkdir -p "%{buildroot}%{_libdir}"
install -m 0755 -p out/Release/build/lib.target/%{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so.%{version}"
ln -s %{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so.%{major}.0"
ln -s %{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so.%{major}"
ln -s %{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so"

# Installing additional development files...
mkdir -p "%{buildroot}%{_includedir}/%{name}/audio"
find . -maxdepth 1 -type f -name "*.h" -exec install -m 0644 -p '{}' %{buildroot}%{_includedir}/%{name} \;
find audio -maxdepth 1 -type f -name "*.h" -exec install -m 0644 -p '{}' %{buildroot}%{_includedir}/%{name}/audio \;

%files -n %{libname}
%{_libdir}/%{name}.so.*

%files -n %{devname}
%{_includedir}/%{name}
%{_libdir}/%{name}.so
