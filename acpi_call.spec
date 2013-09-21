#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

#
# main package.
#
%define		rel	0.3
%define		pname	acpi_call
%define		snap	20130705
Summary:	A linux kernel module that enables calls to ACPI methods through /proc/acpi/call
Name:		acpi_call%{_alt_kernel}
Version:	%{snap}
Release:	0.%{snap}.%{rel}
License:	GPL v2
Group:		Base/Kernel
# snap from "git clone https://github.com/mkottman/acpi_call.git"
Source0:	http://sls.warszawa.pl/%{name}-%{version}.tar.gz
# Source0-md5:	f4eb8bb4d4413a5ae65aa7d77f4112c0
URL:		https://github.com/mkottman/acpi_call
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A linux kernel module that enables calls to ACPI methods through
/proc/acpi/call

%package -n kernel%{_alt_kernel}-misc-acpi_call
Summary:	A linux kernel module that enables calls to ACPI methods through /proc/acpi/call
Release:	0.%{snap}.%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-misc-acpi_call
A linux kernel module that enables calls to ACPI methods through
/proc/acpi/call

%prep
%setup -q -n acpi_call

%build
%if %{with kernel}
%build_kernel_modules -m acpi_call
%endif

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m acpi_call -d misc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-misc-acpi_call
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-acpi_call
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-acpi_call
%defattr(644,root,root,755)
%doc README.md
/lib/modules/%{_kernel_ver}/misc/*.ko*
%endif
