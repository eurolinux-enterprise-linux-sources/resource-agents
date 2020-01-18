#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#






# 
# Since this spec file supports multiple distributions, ensure we
# use the correct group for each.
#

## Whether this platform defaults to using systemd as an init system
## (needs to be evaluated prior to BuildRequires being enumerated and
## installed as it's intended to conditionally select some of these, and
## for that there are only few indicators with varying reliability:
## - presence of systemd-defined macros (when building in a full-fledged
##   environment, which is not the case with ordinary mock-based builds)
## - systemd-aware rpm as manifested with the presence of particular
##   macro (rpm itself will trivially always be present when building)
## - existence of /usr/lib/os-release file, which is something heavily
##   propagated by systemd project
## - when not good enough, there's always a possibility to check
##   particular distro-specific macros (incl. version comparison)
%define systemd_native (%{?_unitdir:1}%{?!_unitdir:0}%{nil \
  } || %{?__transaction_systemd_inhibit:1}%{?!__transaction_systemd_inhibit:0}%{nil \
  } || %(test -f /usr/lib/os-release; test $? -ne 0; echo $?))

%global upstream_prefix ClusterLabs-resource-agents
%global upstream_version e711383f

%global sap_script_prefix sap_cluster_connector
%global sap_script_hash 0015fe2

%global sap_script_package_prefix sap_cluster_connector
%global sap_script_package_hash f3644f5

%global saphana_prefix SAPHanaSR
%global saphana_hash 2067519

%global saphana_scaleout_prefix SAPHanaSR-ScaleOut
%global saphana_scaleout_hash a77e8c6

%global bundled_lib_dir		bundled
# google-cloud-sdk bundle
%global googlecloudsdk		google-cloud-sdk
%global googlecloudsdk_version	206.0.0
%global googlecloudsdk_dir	%{bundled_lib_dir}/%{googlecloudsdk}
# python-pyroute2 bundle
%global pyroute2		pyroute2
%global pyroute2_version	0.4.13
%global pyroute2_dir		%{bundled_lib_dir}/%{pyroute2}
# python-colorama bundle
%global colorama		colorama
%global colorama_version	0.3.3
%global colorama_dir		%{bundled_lib_dir}/%{colorama}
# python-jmespath bundle
%global jmespath		jmespath
%global jmespath_version	0.7.1
%global jmespath_dir		%{bundled_lib_dir}/%{jmespath}
# python-pycryptodome bundle
%global pycryptodome		pycryptodome
%global pycryptodome_version	3.6.4
%global pycryptodome_dir	%{bundled_lib_dir}/%{pycryptodome}
# python-aliyun-sdk-core bundle
%global aliyunsdkcore		aliyun-python-sdk-core
%global aliyunsdkcore_version	2.8.5
%global aliyunsdkcore_dir	%{bundled_lib_dir}/%{aliyunsdkcore}
# python-aliyun-sdk-ecs bundle
%global aliyunsdkecs		aliyun-python-sdk-ecs
%global aliyunsdkecs_version	4.9.3
%global aliyunsdkecs_dir	%{bundled_lib_dir}/%{aliyunsdkecs}
# python-aliyun-sdk-vpc bundle
%global aliyunsdkvpc		aliyun-python-sdk-vpc
%global aliyunsdkvpc_version	3.0.2
%global aliyunsdkvpc_dir	%{bundled_lib_dir}/%{aliyunsdkvpc}
# aliyuncli bundle
%global aliyuncli		aliyun-cli
%global aliyuncli_version	2.1.10
%global aliyuncli_dir		%{bundled_lib_dir}/%{aliyuncli}

# determine the ras-set to process based on configure invokation
%bcond_with rgmanager
%bcond_without linuxha

Name:		resource-agents
Summary:	Open Source HA Reusable Cluster Resource Scripts
Version:	4.1.1
Release:	30%{?dist}
License:	GPLv2+ and LGPLv2+ and ASL 2.0
URL:		https://github.com/ClusterLabs/resource-agents
%if 0%{?fedora} || 0%{?centos_version} || 0%{?rhel}
Group:		System Environment/Base
%else
Group:		Productivity/Clustering/HA
%endif
Source0:	%{upstream_prefix}-%{upstream_version}.tar.gz
Source1:	%{sap_script_prefix}-%{sap_script_hash}.tar.gz
Source2:	%{sap_script_package_prefix}-%{sap_script_package_hash}.tar.gz
Source3:	%{saphana_prefix}-%{saphana_hash}.tar.gz
Source4:	%{saphana_scaleout_prefix}-%{saphana_scaleout_hash}.tar.gz
Source5:	%{googlecloudsdk}-%{googlecloudsdk_version}-linux-x86_64.tar.gz
Source6:	%{pyroute2}-%{pyroute2_version}.tar.gz
Source7:	%{colorama}-%{colorama_version}.tar.gz
Source8:	%{jmespath}-%{jmespath_version}.tar.gz
Source9:	%{pycryptodome}-%{pycryptodome_version}.tar.gz
Source10:	%{aliyunsdkcore}-%{aliyunsdkcore_version}.tar.gz
Source11:	%{aliyunsdkecs}-%{aliyunsdkecs_version}.tar.gz
Source12:	%{aliyunsdkvpc}-%{aliyunsdkvpc_version}.tar.gz
Source13:	%{aliyuncli}-%{aliyuncli_version}.tar.gz
Patch0:		bz1596139-1-nova-compute-wait-NovaEvacuate.patch
Patch1:		bz1470840-LVM-volume_group_check_only.patch
Patch2:		bz1538689-vdo-vol.patch
Patch3:		bz1484920-IPaddr2-monitor_retries.patch
Patch4:		bz1499894-VirtualDomain-stateless-support.patch
Patch5:		bz1568588-1-configure-add-python-path-detection.patch
Patch6:		bz1568588-2-ci-skip-python-agents-in-shellcheck.patch
Patch7:		bz1568588-3-gcp-vpc-move-vip.patch
Patch8:		bz1568588-4-gcp-vpc-move-route.patch
Patch9:		bz1568588-5-python-library.patch
Patch10:	bz1602783-dont-use-ocf_attribute_target-for-metadata.patch
Patch11:	bz1513957-LVM-activate-fix-issue-with-dashes.patch
Patch12:	bz1568588-6-gcp-move-vip-filter-aggregatedlist.patch
Patch13:	bz1568589-1-aliyun-vpc-move-ip.patch
Patch14:	bz1568589-2-aliyun-vpc-move-ip-fixes.patch
Patch15:	bz1568589-3-aliyun-vpc-move-ip-fix-manpage.patch
Patch16:	bz1596139-2-build-add-missing-manpages.patch
Patch17:	bz1568588-7-gcp-stackdriver-logging-note.patch
Patch18:	bz1612828-LVM-fix-missing-dash.patch
Patch19:	bz1606316-lvmlockd-add-cmirrord-support.patch
Patch20:	bz1619428-1-LVM-activate-warn-vg_access_mode.patch
Patch21:	bz1568589-5-aliyun-vpc-move-ip-improve-metadata-manpage.patch
Patch22:	bz1624741-1-aws-vpc-move-ip-avoid-false-positive-monitor.patch
Patch23:	bz1624741-2-aws-vpc-move-ip-avoid-false-positive-monitor.patch
Patch24:	bz1523318-timeout-interval-add-s-suffix.patch
Patch25:	bz1619428-2-LVM-activate-parameters-access-mode-fixes.patch
Patch26:	bz1637823-1-nfsserver-mount-rpc_pipefs.patch
Patch27:	bz1637823-2-nfsserver-var-lib-nfs-fix.patch
Patch28:	bz1641944-rabbitmq-cluster-monitor-mnesia-status.patch
Patch29:	bz1641946-rabbitmq-cluster-fail-when-in-minority-partition.patch
Patch30:	bz1639826-rabbitmq-cluster-fix-stop-regression.patch
Patch31:	bz1647252-vdo-vol-fix-monitor-action.patch
Patch32:	bz1646770-tomcat-use-systemd-when-catalina.sh-unavailable.patch
Patch33:	bz1656368-rabbitmq-cluster-ensure-node-attribures-removed.patch
Patch34:	bz1655655-ocf_log-do-not-log-debug-when-HA_debug-unset.patch
Patch35:	bz1643306-LVM-activate-dont-fail-initial-probe.patch
Patch36:	bz1575095-rabbitmq-cluster-retry-start-cluster-join-fails.patch
Patch37:	bz1659072-1-rabbitmq-cluster-debug-log-mnesia-query-fails.patch
Patch38:	bz1659072-2-rabbitmq-cluster-suppress-additional-output.patch
Patch39:	bz1629357-docker-fix-stop-issues.patch
Patch40:	bz1669137-Route-make-family-parameter-optional.patch
Patch41:	bz1549579-1-clvm-exclusive-mode-support.patch
Patch42:	bz1642069-1-SAPInstance-add-reload-action.patch
Patch43:	bz1642069-2-SAPInstance-improve-profile-detection.patch
Patch44:	bz1642069-3-SAPInstance-metadata-improvements.patch
Patch45:	bz1667413-1-LVM-activate-support-LVs-from-same-VG.patch
Patch46:	bz1667413-2-LVM-activate-only-count-volumes.patch
Patch47:	bz1651790-1-CTDB-explicitly-use-bash-shell.patch
Patch48:	bz1651790-2-CTDB-add-ctdb_max_open_files-parameter.patch
Patch49:	bz1504055-IPsrcaddr-fix-regression-without-NetworkManager.patch
Patch50:	bz1598969-iSCSILogicalUnit-create-iqn-when-it-doesnt-exist.patch
Patch51:	bz1693658-aws-vpc-move-ip-avoid-possible-race-condition.patch
Patch52:	bz1697558-aws-vpc-move-ip-1-multi-route-table-support.patch
Patch53:	bz1697558-aws-vpc-move-ip-2-fix-route-update-multi-NICs.patch
Patch54:	bz1549579-2-ocf_is_true-add-True-to-regexp.patch
Patch55:	bz1363902-SAPHanaSR-monitor-fix-tolower-error.patch

# bundle patches
Patch1000:	bz1568588-7-gcp-bundled.patch
Patch1001:	bz1568588-8-google-cloud-sdk-fixes.patch
Patch1002:	bz1568588-9-google-cloud-sdk-oauth2client-python-rsa-to-cryptography.patch
Patch1003:	bz1568588-10-gcloud-support-info.patch
Patch1004:	bz1568589-4-aliyun-vpc-move-ip-bundled.patch

Obsoletes:	heartbeat-resources <= %{version}
Provides:	heartbeat-resources = %{version}

## Setup/build bits
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Build dependencies
BuildRequires: automake autoconf pkgconfig
BuildRequires: perl python-devel python-setuptools
BuildRequires: libxslt glib2-devel
BuildRequires: which

%if %{systemd_native}
BuildRequires: pkgconfig(systemd)
%endif

%if 0%{?fedora} || 0%{?centos_version} || 0%{?rhel}
#BuildRequires: cluster-glue-libs-devel
BuildRequires: docbook-style-xsl docbook-dtds
%if 0%{?rhel} == 0
BuildRequires: libnet-devel
%endif
%endif

## Runtime deps
# system tools shared by several agents
Requires: /bin/bash /bin/grep /bin/sed /bin/gawk
Requires: /bin/ps /usr/bin/pkill /bin/hostname /bin/netstat
Requires: /usr/sbin/fuser /bin/mount

# Filesystem / fs.sh / netfs.sh
Requires: /sbin/fsck
Requires: /usr/sbin/fsck.ext2 /usr/sbin/fsck.ext3 /usr/sbin/fsck.ext4
Requires: /usr/sbin/fsck.xfs
Requires: /sbin/mount.nfs /sbin/mount.nfs4 /usr/sbin/mount.cifs

# IPaddr2
Requires: /sbin/ip

# LVM / lvm.sh
Requires: /usr/sbin/lvm

# nfsserver / netfs.sh
Requires: /usr/sbin/rpc.nfsd /sbin/rpc.statd /usr/sbin/rpc.mountd

# rgmanager
%if %{with rgmanager}
# ip.sh
Requires: /usr/sbin/ethtool
Requires: /sbin/rdisc /usr/sbin/arping /bin/ping /bin/ping6

# nfsexport.sh
Requires: /sbin/findfs
Requires: /sbin/quotaon /sbin/quotacheck
%endif

## Runtime dependencies required to guarantee heartbeat agents
## are functional
%if %{with linuxha}
# ethmonitor requires the bc calculator
Requires: bc
# tools needed for Filesystem resource
Requires: psmisc
# Tools needed for clvm resource. 
Requires: procps-ng
%endif

%description
A set of scripts to interface with several services to operate in a
High Availability environment for both Pacemaker and rgmanager
service managers.

%ifarch x86_64
%package aliyun
License:	GPLv2+ and LGPLv2+ and ASL 2.0 and BSD and MIT
Summary:	Alibaba Cloud (Aliyun) resource agents
%if 0%{?fedora} || 0%{?centos_version} || 0%{?rhel}
Group:		System Environment/Base
%else
Group:		Productivity/Clustering/HA
%endif
Requires:	%{name} = %{version}-%{release}
# python-colorama bundle
Provides:	bundled(python-%{colorama}) = %{colorama_version}
# python-jmespath bundle
Provides:	bundled(python-jmespath) = %{jmespath_version}
Requires:	python-dateutil >= 1.4
Requires:	python-docutils >= 0.10
# python-pycryptodome bundle
Provides:	bundled(python-%{pycryptodome}) = %{pycryptodome_version}
# python-aliyun-sdk-core bundle
Provides:	bundled(python-aliyun-sdk-core) = %{aliyunsdkcore_version}
# python-aliyun-sdk-ecs bundle
Provides:	bundled(python-aliyun-sdk-ecs) = %{aliyunsdkecs_version}
# python-aliyun-sdk-vpc bundle
Provides:	bundled(python-aliyun-sdk-vpc) = %{aliyunsdkvpc_version}
# aliyuncli bundle
Provides:	bundled(aliyuncli) = %{aliyuncli_version}

%description aliyun
Alibaba Cloud (Aliyun) resource agents allows Alibaba Cloud
(Aliyun) instances to be managed in a cluster environment.
%endif

%ifarch x86_64
%package gcp
License:	GPLv2+ and LGPLv2+ and BSD and ASL 2.0 and MIT and Python
Summary:	Google Cloud Platform resource agents
%if 0%{?fedora} || 0%{?centos_version} || 0%{?rhel}
Group:		System Environment/Base
%else
Group:		Productivity/Clustering/HA
%endif
Requires:	%{name} = %{version}-%{release}
# google-cloud-sdk bundle
Requires:	python-cryptography >= 1.7.2
Provides:	bundled(%{googlecloudsdk}) = %{googlecloudsdk_version}
Provides:	bundled(python-antlr3) = 3.1.1
Provides:	bundled(python-appdirs) = 1.4.0
Provides:	bundled(python-argparse) = 1.2.1
Provides:	bundled(python-chardet) = 2.3.0
Provides:	bundled(python-dateutil) = 2.6.0
Provides:	bundled(python-dulwich) = 0.10.2
Provides:	bundled(python-ipaddress) = 1.0.16
Provides:	bundled(python-ipaddr) = 2.1.11
Provides:	bundled(python-mako) = 1.0.7
Provides:	bundled(python-oauth2client) = 3.0.0
Provides:	bundled(python-prompt_toolkit) = 1.0.13
Provides:	bundled(python-pyasn1) = 0.4.2
Provides:	bundled(python-pyasn1_modules) = 0.2.1
Provides:	bundled(python-pygments) = 2.2.0
Provides:	bundled(python-pyparsing) = 2.1.10
Provides:	bundled(python-requests) = 2.10.0
Provides:	bundled(python-six) = 1.11.0
Provides:	bundled(python-uritemplate) = 3.0.0
Provides:	bundled(python-urllib3) = 1.15.1
Provides:	bundled(python-websocket) = 0.47.0
Provides:	bundled(python-yaml) = 3.12
# python-pyroute2 bundle
Provides:	bundled(%{pyroute2}) = %{pyroute2_version}

%description gcp
The Google Cloud Platform resource agents allows Google Cloud
Platform instances to be managed in a cluster environment.
%endif

%ifarch x86_64 ppc64le
%package sap
License:	GPLv2+
Summary:	SAP cluster resource agents and connector script
%if 0%{?fedora} || 0%{?centos_version} || 0%{?rhel}
Group:		System Environment/Base
%else
Group:		Productivity/Clustering/HA
%endif
Requires:	%{name} = %{version}-%{release}
Requires:	perl

%description sap
The SAP resource agents and connector script interface with 
Pacemaker to allow SAP instances to be managed in a cluster
environment.
%endif

%ifarch x86_64 ppc64le
%package sap-hana
License:	GPLv2+
Summary:	SAP HANA cluster resource agents
%if 0%{?fedora} || 0%{?centos_version} || 0%{?rhel}
Group:		System Environment/Base
%else
Group:		Productivity/Clustering/HA
%endif
Requires:	%{name} = %{version}-%{release}
Requires:	perl

%description sap-hana
The SAP HANA resource agents interface with  Pacemaker to allow
SAP instances to be managed in a cluster environment.
%endif

%ifarch x86_64 ppc64le
%package sap-hana-scaleout
License:	GPLv2+
Summary:	SAP HANA Scale-Out cluster resource agents
Version:	0.163.2
Release:	7%{?rcver:%{rcver}}%{?numcomm:.%{numcomm}}%{?alphatag:.%{alphatag}}%{?dirty:.%{dirty}}%{?dist}
%if 0%{?fedora} || 0%{?centos_version} || 0%{?rhel}
Group:		System Environment/Base
%else
Group:		Productivity/Clustering/HA
%endif
Requires:	resource-agents >= 4.1.1-25
Requires:	perl

%description sap-hana-scaleout
The SAP HANA Scale-Out resource agents interface with Pacemaker
to allow SAP HANA Scale-Out instances to be managed in a cluster
environment.
%endif

%ifarch x86_64 ppc64le
%package -n sap-cluster-connector
License:	GPLv2+
Summary:	SAP cluster connector script
Version:	3.0.1
Release:	7%{?rcver:%{rcver}}%{?numcomm:.%{numcomm}}%{?alphatag:.%{alphatag}}%{?dirty:.%{dirty}}%{?dist}
%if 0%{?fedora} || 0%{?centos_version} || 0%{?rhel}
Group:		System Environment/Base
%else
Group:		Productivity/Clustering/HA
%endif
Requires:	resource-agents-sap >= 4.1.1-25
Requires:	perl

%description -n sap-cluster-connector
The SAP connector script interface with Pacemaker to allow SAP
instances to be managed in a cluster environment.
%endif

%prep
%if 0%{?suse_version} == 0 && 0%{?fedora} == 0 && 0%{?centos_version} == 0 && 0%{?rhel} == 0
%{error:Unable to determine the distribution/version. This is generally caused by missing /etc/rpm/macros.dist. Please install the correct build packages or define the required macros manually.}
exit 1
%endif
%setup -q -n %{upstream_prefix}-%{upstream_version}
%setup -T -D -a 1 -n %{upstream_prefix}-%{upstream_version}
%setup -T -D -a 2 -n %{upstream_prefix}-%{upstream_version}
%setup -T -D -a 3 -n %{upstream_prefix}-%{upstream_version}
%setup -T -D -a 4 -n %{upstream_prefix}-%{upstream_version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1
%patch50 -p1
%patch51 -p1 -F2
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1

# add SAPHana agents to Makefile.am
mv %{saphana_prefix}-%{saphana_hash}/SAPHana/ra/SAPHana* heartbeat
mv %{saphana_scaleout_prefix}-%{saphana_scaleout_hash}/SAPHana/ra/SAPHanaController heartbeat
mv %{saphana_scaleout_prefix}-%{saphana_scaleout_hash}/SAPHana/ra/SAPHanaTopology heartbeat/SAPHanaTopologyScaleOut
sed -i -e 's/\(<resource-agent name="SAPHanaTopology\)/\1ScaleOut/' heartbeat/SAPHanaTopologyScaleOut
sed -i -e '/			SAPInstance		\\/a\			SAPHana			\\\n			SAPHanaTopology		\\\n			SAPHanaController	\\\n			SAPHanaTopologyScaleOut	\\' heartbeat/Makefile.am
sed -i -e '/                          ocf_heartbeat_SAPInstance.7 \\/a\                          ocf_heartbeat_SAPHana.7 \\\n                          ocf_heartbeat_SAPHanaTopology.7 \\\n                          ocf_heartbeat_SAPHanaController.7 \\\n                          ocf_heartbeat_SAPHanaTopologyScaleOut.7 \\' doc/man/Makefile.am

# bundles
mkdir -p %{bundled_lib_dir}

# google-cloud-sdk bundle
%ifarch x86_64
tar -xzf %SOURCE5 -C %{bundled_lib_dir}
# gcp*: append bundled-directory to search path, gcloud-ra
%patch1000 -p1
# google-cloud-sdk fixes
%patch1001 -p1
# replace python-rsa with python-cryptography
%patch1002 -p1
# gcloud support info
%patch1003 -p1
# rename gcloud
mv %{googlecloudsdk_dir}/bin/gcloud %{googlecloudsdk_dir}/bin/gcloud-ra
# keep googleapiclient
mv %{googlecloudsdk_dir}/platform/bq/third_party/googleapiclient %{googlecloudsdk_dir}/lib/third_party
# only keep gcloud
rm -rf %{googlecloudsdk_dir}/bin/{bootstrapping,bq,dev_appserver.py,docker-credential-gcloud,endpointscfg.py,git-credential-gcloud.sh,gsutil,java_dev_appserver.sh} %{googlecloudsdk_dir}/{completion.*,deb,install.*,path.*,platform,properties,RELEASE_NOTES,rpm,VERSION}
# remove Python 3 code
rm -rf %{googlecloudsdk_dir}/lib/third_party/*/python3
# remove python-rsa
rm -rf %{googlecloudsdk_dir}/lib/third_party/rsa
# remove grpc
rm -rf %{googlecloudsdk_dir}/lib/third_party/grpc
# docs/licenses
cp %{googlecloudsdk_dir}/README %{googlecloudsdk}_README
cp %{googlecloudsdk_dir}/lib/third_party/argparse/README.txt %{googlecloudsdk}_argparse_README.txt
cp %{googlecloudsdk_dir}/LICENSE %{googlecloudsdk}_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/httplib2/LICENSE %{googlecloudsdk}_httplib2_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/contextlib2/LICENSE %{googlecloudsdk}_contextlib2_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/concurrent/LICENSE %{googlecloudsdk}_concurrent_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/yaml/LICENSE %{googlecloudsdk}_yaml_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/pyu2f/LICENSE %{googlecloudsdk}_pyu2f_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/ml_sdk/LICENSE %{googlecloudsdk}_ml_sdk_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/ml_sdk/pkg/LICENSE %{googlecloudsdk}_pkg_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/ipaddr/LICENSE %{googlecloudsdk}_ipaddr_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/urllib3/LICENSE %{googlecloudsdk}_urllib3_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/ipaddress/LICENSE %{googlecloudsdk}_ipaddress_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/requests/LICENSE %{googlecloudsdk}_requests_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/docker/LICENSE %{googlecloudsdk}_docker_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/monotonic/LICENSE %{googlecloudsdk}_monotonic_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/websocket/LICENSE %{googlecloudsdk}_websocket_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/fasteners/LICENSE %{googlecloudsdk}_fasteners_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/wcwidth/LICENSE %{googlecloudsdk}_wcwidth_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/pygments/LICENSE %{googlecloudsdk}_pygments_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/oauth2client/LICENSE %{googlecloudsdk}_oauth2client_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/uritemplate/LICENSE %{googlecloudsdk}_uritemplate_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/dateutil/LICENSE %{googlecloudsdk}_dateutil_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/dulwich/LICENSE %{googlecloudsdk}_dulwich_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/mako/LICENSE %{googlecloudsdk}_mako_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/packaging/LICENSE %{googlecloudsdk}_packaging_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/socks/LICENSE %{googlecloudsdk}_socks_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/antlr3/LICENSE %{googlecloudsdk}_antlr3_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/argparse/LICENSE.txt %{googlecloudsdk}_argparse_LICENSE.txt
cp %{googlecloudsdk_dir}/lib/third_party/chardet/LICENSE %{googlecloudsdk}_chardet_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/ruamel/LICENSE %{googlecloudsdk}_ruamel_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/appdirs/LICENSE %{googlecloudsdk}_appdirs_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/argcomplete/LICENSE %{googlecloudsdk}_argcomplete_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/pyasn1_modules/LICENSE %{googlecloudsdk}_pyasn1_modules_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/typing/LICENSE %{googlecloudsdk}_typing_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/setuptools/LICENSE %{googlecloudsdk}_setuptools_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/google/LICENSE %{googlecloudsdk}_google_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/google/protobuf/LICENSE %{googlecloudsdk}_protobuf_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/six/LICENSE %{googlecloudsdk}_six_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/dns/LICENSE %{googlecloudsdk}_dns_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/enum/LICENSE %{googlecloudsdk}_enum_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/gae_ext_runtime/LICENSE %{googlecloudsdk}_gae_ext_runtime_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/fancy_urllib/LICENSE %{googlecloudsdk}_fancy_urllib_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/pyasn1/LICENSE %{googlecloudsdk}_pyasn1_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/apitools/LICENSE %{googlecloudsdk}_apitools_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/containerregistry/LICENSE %{googlecloudsdk}_containerregistry_LICENSE
cp %{googlecloudsdk_dir}/lib/third_party/prompt_toolkit/LICENSE %{googlecloudsdk}_prompt_toolkit_LICENSE

# python-pyroute2 bundle
tar -xzf %SOURCE6 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/%{pyroute2}-%{pyroute2_version} %{pyroute2_dir}
cp %{pyroute2_dir}/README.md %{pyroute2}_README.md
cp %{pyroute2_dir}/README.license.md %{pyroute2}_README.license.md
cp %{pyroute2_dir}/LICENSE.Apache.v2 %{pyroute2}_LICENSE.Apache.v2
cp %{pyroute2_dir}/LICENSE.GPL.v2 %{pyroute2}_LICENSE.GPL.v2

# python-colorama bundle
tar -xzf %SOURCE7 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/%{colorama}-%{colorama_version} %{colorama_dir}
cp %{colorama_dir}/LICENSE.txt %{colorama}_LICENSE.txt
cp %{colorama_dir}/README.rst %{colorama}_README.rst

pushd %{colorama_dir}
# remove bundled egg-info
rm -rf *.egg-info
popd

# python-jmespath bundle
tar -xzf %SOURCE8 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/jmespath.py-%{jmespath_version} %{jmespath_dir}
cp %{jmespath_dir}/LICENSE.txt %{jmespath}_LICENSE.txt
cp %{jmespath_dir}/README.rst %{jmespath}_README.rst

pushd %{jmespath_dir}
rm -rf jmespath.egg-info
popd

# python-pycryptodome bundle
tar -xzf %SOURCE9 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/%{pycryptodome}-%{pycryptodome_version} %{pycryptodome_dir}
cp %{pycryptodome_dir}/README.rst %{pycryptodome}_README.rst
cp %{pycryptodome_dir}/LICENSE.rst %{pycryptodome}_LICENSE.rst

# python-aliyun-sdk-core bundle
tar -xzf %SOURCE10 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/%{aliyunsdkcore}-%{aliyunsdkcore_version} %{aliyunsdkcore_dir}
cp %{aliyunsdkcore_dir}/README.rst %{aliyunsdkcore}_README.rst

# python-aliyun-sdk-ecs bundle
tar -xzf %SOURCE11 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/%{aliyunsdkecs}-%{aliyunsdkecs_version} %{aliyunsdkecs_dir}
cp %{aliyunsdkecs_dir}/README.rst %{aliyunsdkecs}_README.rst

# python-aliyun-sdk-vpc bundle
tar -xzf %SOURCE12 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/%{aliyunsdkvpc}-%{aliyunsdkvpc_version} %{aliyunsdkvpc_dir}
cp %{aliyunsdkvpc_dir}/README.rst %{aliyunsdkvpc}_README.rst

# aliyuncli bundle
tar -xzf %SOURCE13 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/%{aliyuncli}-%{aliyuncli_version} %{aliyuncli_dir}
cp %{aliyuncli_dir}/README.rst %{aliyuncli}_README.rst
cp %{aliyuncli_dir}/LICENSE %{aliyuncli}_LICENSE
# aliyun*: use bundled libraries
%patch1004 -p1
%endif

%build
if [ ! -f configure ]; then
	./autogen.sh
fi

%if 0%{?fedora} >= 11 || 0%{?centos_version} > 5 || 0%{?rhel} > 5
CFLAGS="$(echo '%{optflags}')"
%global conf_opt_fatal "--enable-fatal-warnings=no"
%else
CFLAGS="${CFLAGS} ${RPM_OPT_FLAGS}"
%global conf_opt_fatal "--enable-fatal-warnings=yes"
%endif

%if %{with rgmanager}
%global rasset rgmanager
%endif
%if %{with linuxha}
%global rasset linux-ha
%endif
%if %{with rgmanager} && %{with linuxha}
%global rasset all
%endif

export CFLAGS

chmod 755 heartbeat/nova-compute-wait
chmod 755 heartbeat/NovaEvacuate
chmod 755 heartbeat/vdo-vol

%configure BASH_SHELL="/bin/bash" \
	%{conf_opt_fatal} \
%if %{defined _unitdir}
    --with-systemdsystemunitdir=%{_unitdir} \
%endif
%if %{defined _tmpfilesdir}
    --with-systemdtmpfilesdir=%{_tmpfilesdir} \
%endif
	--with-pkg-name=%{name} \
	--with-ras-set=%{rasset} \
	--with-ocft-cases=fedora

%if %{defined jobs}
JFLAGS="$(echo '-j%{jobs}')"
%else
JFLAGS="$(echo '%{_smp_mflags}')"
%endif

make $JFLAGS

# python-pyroute2 bundle
%ifarch x86_64
pushd %{pyroute2_dir}
%{__python2} setup.py build
popd

# python-colorama bundle
pushd %{colorama_dir}
%{__python2} setup.py build
popd

# python-jmespath bundle
pushd %{jmespath_dir}
CFLAGS="%{optflags}" %{__python} setup.py %{?py_setup_args} build --executable="%{__python2} -s"
popd

# python-pycryptodome bundle
pushd %{pycryptodome_dir}
%{__python2} setup.py build
popd

# python-aliyun-sdk-core bundle
pushd %{aliyunsdkcore_dir}
%{__python2} setup.py build
popd

# python-aliyun-sdk-ecs bundle
pushd %{aliyunsdkecs_dir}
%{__python2} setup.py build
popd

# python-aliyun-sdk-vpc bundle
pushd %{aliyunsdkvpc_dir}
%{__python2} setup.py build
popd

# aliyuncli bundle
pushd %{aliyuncli_dir}
%{__python2} setup.py build
popd
%endif

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

test -d %{buildroot}/%{_sbindir} || mkdir %{buildroot}/%{_sbindir}
cp %{sap_script_prefix}-%{sap_script_hash}/redhat/sap_redhat_cluster_connector %{buildroot}/%{_sbindir}

test -d %{buildroot}/%{_bindir} || mkdir %{buildroot}/%{_bindir}
cp %{sap_script_package_prefix}-%{sap_script_package_hash}/redhat/sap_cluster_connector %{buildroot}/%{_bindir}
mkdir %{buildroot}/%{_datadir}/sap_cluster_connector
cp -rv %{sap_script_package_prefix}-%{sap_script_package_hash}/redhat/{run_checks,checks} %{buildroot}/%{_datadir}/sap_cluster_connector
gzip %{sap_script_package_prefix}-%{sap_script_package_hash}/redhat/man/*.8
cp %{sap_script_package_prefix}-%{sap_script_package_hash}/redhat/man/*.8.gz %{buildroot}/%{_mandir}/man8

install -m 0755 %{saphana_scaleout_prefix}-%{saphana_scaleout_hash}/SAPHana/bin/{SAPHanaSR-monitor,SAPHanaSR-showAttr} %{buildroot}/%{_sbindir}
mkdir %{buildroot}/%{_usr}/lib/SAPHanaSR-ScaleOut
install -m 0444 %{saphana_scaleout_prefix}-%{saphana_scaleout_hash}/SAPHana/test/SAPHanaSRTools.pm %{buildroot}/%{_usr}/lib/SAPHanaSR-ScaleOut/SAPHanaSRTools.pm
mkdir -p %{buildroot}/%{_datadir}/SAPHanaSR-ScaleOut/samples
install -m 0644 %{saphana_scaleout_prefix}-%{saphana_scaleout_hash}/SAPHana/srHook/SAPHanaSR.py %{buildroot}/%{_datadir}/SAPHanaSR-ScaleOut
install -m 0444 %{saphana_scaleout_prefix}-%{saphana_scaleout_hash}/SAPHana/crmconfig/* %{buildroot}/%{_datadir}/SAPHanaSR-ScaleOut/samples
install -m 0444 %{saphana_scaleout_prefix}-%{saphana_scaleout_hash}/SAPHana/srHook/global.ini %{buildroot}/%{_datadir}/SAPHanaSR-ScaleOut/samples
gzip %{saphana_scaleout_prefix}-%{saphana_scaleout_hash}/SAPHana/man/SAPHanaSR*.?
cp %{saphana_scaleout_prefix}-%{saphana_scaleout_hash}/SAPHana/man/SAPHanaSR*.7.gz %{buildroot}/%{_mandir}/man7
cp %{saphana_scaleout_prefix}-%{saphana_scaleout_hash}/SAPHana/man/SAPHanaSR*.8.gz %{buildroot}/%{_mandir}/man8


# google-cloud-sdk bundle
%ifarch x86_64
pushd %{googlecloudsdk_dir}
mkdir -p %{buildroot}/usr/lib/%{name}/%{googlecloudsdk_dir}
cp -a bin data lib %{buildroot}/usr/lib/%{name}/%{googlecloudsdk_dir}
test -d %{buildroot}/%{_bindir} || mkdir %{buildroot}/%{_bindir}
ln -s /usr/lib/%{name}/%{googlecloudsdk_dir}/bin/gcloud-ra %{buildroot}/%{_bindir}
popd

# python-pyroute2 bundle
pushd %{pyroute2_dir}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/%{name}/%{bundled_lib_dir}
popd
# python-colorama bundle
pushd %{colorama_dir}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/%{name}/%{bundled_lib_dir}
popd

# python-jmespath bundle
pushd %{jmespath_dir}
CFLAGS="%{optflags}" %{__python} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/%{name}/%{bundled_lib_dir}
popd
rm %{buildroot}/%{_bindir}/jp.py

# python-pycryptodome bundle
pushd %{pycryptodome_dir}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/%{name}/%{bundled_lib_dir}
popd

# python-aliyun-sdk-core bundle
pushd %{aliyunsdkcore_dir}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/%{name}/%{bundled_lib_dir}
popd

# python-aliyun-sdk-ecs bundle
pushd %{aliyunsdkecs_dir}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/%{name}/%{bundled_lib_dir}
popd

# python-aliyun-sdk-vpc bundle
pushd %{aliyunsdkvpc_dir}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/%{name}/%{bundled_lib_dir}
popd

# aliyuncli bundle
pushd %{aliyuncli_dir}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/%{name}/%{bundled_lib_dir}
sed -i -e "/^import sys/asys.path.insert(0, '/usr/lib/%{name}/%{bundled_lib_dir}')" %{buildroot}/%{_bindir}/aliyuncli
mv %{buildroot}/%{_bindir}/aliyuncli %{buildroot}/%{_bindir}/aliyuncli-ra
# aliyun_completer / aliyun_zsh_complete.sh
rm %{buildroot}/%{_bindir}/aliyun_*
popd
%endif

## tree fixup
# remove docs (there is only one and they should come from doc sections in files)
rm -rf %{buildroot}/usr/share/doc/resource-agents

##
# Create symbolic link between IPAddr and IPAddr2
##
rm -f %{buildroot}/usr/lib/ocf/resource.d/heartbeat/IPaddr
ln -s /usr/lib/ocf/resource.d/heartbeat/IPaddr2 %{buildroot}/usr/lib/ocf/resource.d/heartbeat/IPaddr

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING COPYING.GPLv3 ChangeLog
%if %{with linuxha}
%doc doc/README.webapps
%doc %{_datadir}/%{name}/ra-api-1.dtd
%doc %{_datadir}/%{name}/metadata.rng
%endif

%if %{with rgmanager}
%{_datadir}/cluster
%{_sbindir}/rhev-check.sh
%endif

%if %{with linuxha}
%dir /usr/lib/ocf
%dir /usr/lib/ocf/resource.d
%dir /usr/lib/ocf/lib

/usr/lib/ocf/lib/heartbeat

/usr/lib/ocf/resource.d/heartbeat
/usr/lib/ocf/resource.d/openstack
%if %{with rgmanager}
/usr/lib/ocf/resource.d/redhat
%endif

%if %{defined _unitdir}
%{_unitdir}/resource-agents-deps.target
%endif
%if %{defined _tmpfilesdir}
%{_tmpfilesdir}/%{name}.conf
%endif

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/ocft
%{_datadir}/%{name}/ocft/configs
%{_datadir}/%{name}/ocft/caselib
%{_datadir}/%{name}/ocft/README
%{_datadir}/%{name}/ocft/README.zh_CN
%{_datadir}/%{name}/ocft/helpers.sh
%exclude %{_datadir}/%{name}/ocft/runocft
%exclude %{_datadir}/%{name}/ocft/runocft.prereq

%{_sbindir}/ocft

%{_includedir}/heartbeat

%dir %attr (1755, root, root)	%{_var}/run/resource-agents

%{_mandir}/man7/*.7*

###
# Supported, but in another sub package
###
%exclude %{_sbindir}/sap_redhat_cluster_connector
%exclude %{_bindir}/sap_cluster_connector
%exclude %{_sbindir}/SAPHanaSR*
%exclude /usr/lib/ocf/resource.d/heartbeat/SAP*
%exclude /usr/lib/ocf/lib/heartbeat/sap*
%exclude %{_mandir}/man7/*SAP*
%exclude %{_mandir}/man8/*SAP*
%exclude %{_usr}/lib/SAPHanaSR-ScaleOut
%exclude %{_datadir}/SAPHanaSR-ScaleOut
%exclude %{_mandir}/man8/sap_cluster_connector*
%exclude %{_datadir}/sap_cluster_connector
%exclude /usr/lib/ocf/resource.d/heartbeat/gcp*
%exclude %{_mandir}/man7/*gcp*
%exclude /usr/lib/%{name}

###
# Unsupported
###
%exclude /usr/lib/ocf/resource.d/heartbeat/AoEtarget
%exclude /usr/lib/ocf/resource.d/heartbeat/AudibleAlarm
%exclude /usr/lib/ocf/resource.d/heartbeat/ClusterMon
%exclude /usr/lib/ocf/resource.d/heartbeat/EvmsSCC
%exclude /usr/lib/ocf/resource.d/heartbeat/Evmsd
%exclude /usr/lib/ocf/resource.d/heartbeat/ICP
%exclude /usr/lib/ocf/resource.d/heartbeat/LinuxSCSI
%exclude /usr/lib/ocf/resource.d/heartbeat/ManageRAID
%exclude /usr/lib/ocf/resource.d/heartbeat/ManageVE
%exclude /usr/lib/ocf/resource.d/heartbeat/Pure-FTPd
%exclude /usr/lib/ocf/resource.d/heartbeat/Raid1
%exclude /usr/lib/ocf/resource.d/heartbeat/ServeRAID
%exclude /usr/lib/ocf/resource.d/heartbeat/SphinxSearchDaemon
%exclude /usr/lib/ocf/resource.d/heartbeat/Stateful
%exclude /usr/lib/ocf/resource.d/heartbeat/SysInfo
%exclude /usr/lib/ocf/resource.d/heartbeat/VIPArip
%exclude /usr/lib/ocf/resource.d/heartbeat/WAS
%exclude /usr/lib/ocf/resource.d/heartbeat/WAS6
%exclude /usr/lib/ocf/resource.d/heartbeat/WinPopup
%exclude /usr/lib/ocf/resource.d/heartbeat/Xen
%exclude /usr/lib/ocf/resource.d/heartbeat/anything
%exclude /usr/lib/ocf/resource.d/heartbeat/asterisk
%exclude /usr/lib/ocf/resource.d/heartbeat/aws-vpc-route53
%exclude /usr/lib/ocf/resource.d/heartbeat/dnsupdate
%exclude /usr/lib/ocf/resource.d/heartbeat/eDir88
%exclude /usr/lib/ocf/resource.d/heartbeat/fio
%exclude /usr/lib/ocf/resource.d/heartbeat/ids
%exclude /usr/lib/ocf/resource.d/heartbeat/iface-bridge
%exclude /usr/lib/ocf/resource.d/heartbeat/ipsec
%exclude /usr/lib/ocf/resource.d/heartbeat/jira
%exclude /usr/lib/ocf/resource.d/heartbeat/kamailio
%exclude /usr/lib/ocf/resource.d/heartbeat/lxd-info
%exclude /usr/lib/ocf/resource.d/heartbeat/machine-info
%exclude /usr/lib/ocf/resource.d/heartbeat/mariadb
%exclude /usr/lib/ocf/resource.d/heartbeat/minio
%exclude /usr/lib/ocf/resource.d/heartbeat/mpathpersist
%exclude /usr/lib/ocf/resource.d/heartbeat/iscsi
%exclude /usr/lib/ocf/resource.d/heartbeat/jboss
%exclude /usr/lib/ocf/resource.d/heartbeat/ldirectord
%exclude /usr/lib/ocf/resource.d/heartbeat/lxc
%exclude /usr/lib/ocf/resource.d/heartbeat/openstack-cinder-volume
%exclude /usr/lib/ocf/resource.d/heartbeat/openstack-floating-ip
%exclude /usr/lib/ocf/resource.d/heartbeat/openstack-info
%exclude /usr/lib/ocf/resource.d/heartbeat/ovsmonitor
%exclude /usr/lib/ocf/resource.d/heartbeat/pgagent
%exclude /usr/lib/ocf/resource.d/heartbeat/pingd
%exclude /usr/lib/ocf/resource.d/heartbeat/pound
%exclude /usr/lib/ocf/resource.d/heartbeat/proftpd
%exclude /usr/lib/ocf/resource.d/heartbeat/rkt
%exclude /usr/lib/ocf/resource.d/heartbeat/scsi2reservation
%exclude /usr/lib/ocf/resource.d/heartbeat/sfex
%exclude /usr/lib/ocf/resource.d/heartbeat/sg_persist
%exclude /usr/lib/ocf/resource.d/heartbeat/syslog-ng
%exclude /usr/lib/ocf/resource.d/heartbeat/varnish
%exclude /usr/lib/ocf/resource.d/heartbeat/vmware
%exclude /usr/lib/ocf/resource.d/heartbeat/zabbixserver
%exclude /usr/lib/ocf/resource.d/heartbeat/mysql-proxy
%exclude /usr/lib/ocf/resource.d/heartbeat/rsyslog
%exclude /usr/lib/ocf/resource.d/heartbeat/vsftpd
%exclude /usr/lib/ocf/resource.d/heartbeat/ZFS
%exclude %{_mandir}/man7/ocf_heartbeat_AoEtarget.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_AudibleAlarm.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_ClusterMon.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_EvmsSCC.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_Evmsd.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_ICP.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_IPaddr.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_LinuxSCSI.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_ManageRAID.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_ManageVE.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_Pure-FTPd.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_Raid1.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_ServeRAID.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_SphinxSearchDaemon.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_Stateful.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_SysInfo.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_VIPArip.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_WAS.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_WAS6.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_WinPopup.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_Xen.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_anything.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_asterisk.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_aws-vpc-route53.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_dnsupdate.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_eDir88.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_fio.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_ids.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_iface-bridge.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_ipsec.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_iscsi.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_jboss.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_jira.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_kamailio.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_lxc.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_lxd-info.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_machine-info.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_mariadb.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_minio.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_mpathpersist.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_openstack-cinder-volume.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_openstack-floating-ip.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_openstack-info.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_ovsmonitor.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_pgagent.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_pingd.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_pound.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_proftpd.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_rkt.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_scsi2reservation.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_sfex.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_sg_persist.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_syslog-ng.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_varnish.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_vmware.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_vsftpd.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_zabbixserver.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_mysql-proxy.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_rsyslog.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_ZFS.7.gz

###
# Other excluded files.
###
# This tool has to be updated for the new pacemaker lrmd.
%exclude %{_sbindir}/ocf-tester
%exclude %{_mandir}/man8/ocf-tester.8*
# ldirectord is not supported
%exclude /etc/ha.d/resource.d/ldirectord
%exclude /etc/init.d/ldirectord
%exclude %{_unitdir}/ldirectord.service
%exclude /etc/logrotate.d/ldirectord
%exclude /usr/sbin/ldirectord
%exclude %{_mandir}/man8/ldirectord.8.gz

# For compatability with pre-existing agents
%dir %{_sysconfdir}/ha.d
%{_sysconfdir}/ha.d/shellfuncs

%{_libexecdir}/heartbeat
%endif

%if %{with rgmanager}
%post -n resource-agents
ccs_update_schema > /dev/null 2>&1 ||:
%endif

%ifarch x86_64
%files aliyun
%doc aliyun*_README* %{colorama}_README.rst %{jmespath}_README.rst %{pycryptodome}_README.rst
%license %{aliyuncli}_LICENSE %{colorama}_LICENSE.txt %{jmespath}_LICENSE.txt %{pycryptodome}_LICENSE.rst
%defattr(-,root,root)
/usr/lib/ocf/resource.d/heartbeat/aliyun-vpc-move-ip*
%{_mandir}/man7/*aliyun-vpc-move-ip*
# bundle
%{_bindir}/aliyuncli-ra
%dir /usr/lib/%{name}
/usr/lib/%{name}/%{bundled_lib_dir}/*colorama*
/usr/lib/%{name}/%{bundled_lib_dir}/*jmespath*
/usr/lib/%{name}/%{bundled_lib_dir}/pycryptodome*
/usr/lib/%{name}/%{bundled_lib_dir}/Crypto
/usr/lib/%{name}/%{bundled_lib_dir}/aliyun*
%endif

%ifarch x86_64
%files gcp
%doc %{googlecloudsdk}_*README*
%license %{googlecloudsdk}_*LICENSE*
%doc %{pyroute2}_README*
%license %{pyroute2}_LICENSE*
%defattr(-,root,root)
/usr/lib/ocf/resource.d/heartbeat/gcp-vpc-move-vip*
%{_mandir}/man7/*gcp-vpc-move-vip*
/usr/lib/ocf/resource.d/heartbeat/gcp-vpc-move-route*
%{_mandir}/man7/*gcp-vpc-move-route*
# bundle
%{_bindir}/gcloud-ra
%dir /usr/lib/%{name}
/usr/lib/%{name}/%{bundled_lib_dir}
%exclude /usr/lib/%{name}/%{bundled_lib_dir}/colorama*
%exclude /usr/lib/%{name}/%{bundled_lib_dir}/*jmespath*
%exclude /usr/lib/%{name}/%{bundled_lib_dir}/pycryptodome*
%exclude /usr/lib/%{name}/%{bundled_lib_dir}/Crypto
%exclude /usr/lib/%{name}/%{bundled_lib_dir}/aliyun*
%exclude /usr/lib/%{name}/%{bundled_lib_dir}/integration
%endif

%ifarch x86_64 ppc64le
%files sap
%defattr(-,root,root)
%{_sbindir}/sap_redhat_cluster_connector
/usr/lib/ocf/resource.d/heartbeat/SAP*
/usr/lib/ocf/lib/heartbeat/sap*
%{_mandir}/man7/*SAP*
%exclude %{_mandir}/man7/*SAPHana*
%exclude /usr/lib/ocf/resource.d/heartbeat/SAPHana*
%endif

%ifarch x86_64 ppc64le
%files sap-hana
%defattr(-,root,root)
/usr/lib/ocf/resource.d/heartbeat/SAPHana
/usr/lib/ocf/resource.d/heartbeat/SAPHanaTopology
%{_mandir}/man7/*SAPHana.*
%{_mandir}/man7/*SAPHanaTopology.*
%endif

%ifarch x86_64 ppc64le
%files sap-hana-scaleout
%defattr(-,root,root)
/usr/lib/ocf/resource.d/heartbeat/SAPHanaController
/usr/lib/ocf/resource.d/heartbeat/SAPHanaTopologyScaleOut
%{_mandir}/man7/*SAPHanaController*
%{_mandir}/man7/*SAPHanaTopologyScaleOut*
%{_sbindir}/SAPHanaSR*
%{_mandir}/man7/SAPHanaSR*
%{_mandir}/man8/SAPHanaSR*
%{_usr}/lib/SAPHanaSR-ScaleOut
%{_datadir}/SAPHanaSR-ScaleOut
%endif

%ifarch x86_64 ppc64le
%files -n sap-cluster-connector
%defattr(-,root,root)
%{_bindir}/sap_cluster_connector
%{_mandir}/man8/sap_cluster_connector*
%{_datadir}/sap_cluster_connector
%endif

%changelog
* Thu Jun 27 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-30
- resource-agents-sap-hana-scaleout: new subpackage

  Resolves: rhbz#1363902

* Tue Jun 25 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-27
- sap-cluster-connector: new subpackage

  Resolves: rhbz#1710956

* Tue Jun 18 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-24
- clvm: support exclusive mode

  Resolves: rhbz#1549579

* Mon May 20 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-23
- aws-vpc-move-ip: add multi route-table support and fix issue
  w/multiple NICs

  Resolves: rhbz#1697558

* Fri Apr  5 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-22
- IPsrcaddr: make proto optional to fix regression when used without
  NetworkManager

  Resolves: rhbz#1504055

* Thu Mar 28 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-21
- aws-vpc-move-ip: use "--query" to avoid a possible race condition

  Resolves: rhbz#1693658

* Tue Mar 26 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-20
- IPsrcaddr: add proto and table parameters
- iSCSILogicalUnit: only create iqn when it doesnt exist

  Resolves: rhbz#1504055
  Resolves: rhbz#1598969

* Thu Feb 28 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-19
- CTDB: add ctdb_max_open_files parameter

  Resolves: rhbz#1651790

* Wed Feb 27 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-18
- SAPInstance: add reload-action
- LVM-activate: support LVs from same VG
- Remove grpc from bundle

  Resolves: rhbz#1642069
  Resolves: rhbz#1667413
  Resolves: rhbz#1683629

* Thu Jan 24 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-17
- Route: make family parameter optional

  Resolves: rhbz#1669137

* Thu Jan 17 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-16
- rabbitmq-cluster: suppress additional output
- docker: fix stop issues

  Resolves: rhbz#1659072
  Resolves: rhbz#1629357

* Thu Jan 17 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-15
- rabbitmq-cluster: ensure node attributes are removed
- ocf_log: do not log debug messages when HA_debug unset
- LVM-activate: dont fail initial probe
- rabbitmq-cluster: retry start when cluster join fails

  Resolves: rhbz#1656368
  Resolves: rhbz#1655655
  Resolves: rhbz#1643306
  Resolves: rhbz#1575095

* Wed Nov  7 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-14
- rabbitmq-cluster: fix stop regression
- vdo-vol: fix monitor-action
- tomcat: use systemd when catalina.sh is unavailable

  Resolves: rhbz#1639826
  Resolves: rhbz#1647252
  Resolves: rhbz#1646770

* Tue Oct 23 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-12.5
- rabbitmq-cluster: get cluster status from mnesia during monitor
- rabbitmq-cluster: fail monitor when node is in minority partition

  Resolves: rhbz#1641944
  Resolves: rhbz#1641946

* Thu Oct 11 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-12.4
- nfsserver: mount rpc_pipefs

  Resolves: rhbz#1637823

* Wed Sep 26 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-12
- LVM-activate: fail monitor-action when using invalid access-mode

  Resolves: rhbz#1619428

* Wed Sep  5 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-10
- aws-vpc-move-ip: avoid false positive monitor result on initial probe
- timeout/interval add "s"-suffix

  Resolves: rhbz#1624741
  Resolves: rhbz#1523318

* Fri Aug 31 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-9
- aliyun-vpc-move-ip: improve metadata and manpage

  Resolves: rhbz#1568589

* Thu Aug 23 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-8
- lvmlockd: add cmirrord support
- LVM-activate: warn about incorrect vg_access_mode

  Resolves: rhbz#1606316
  Resolves: rhbz#1619428

* Thu Aug 16 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-7
- aliyun-vpc-move-ip: new resource agent for Alibaba Cloud (Aliyun)

  Resolves: rhbz#1568589

* Wed Aug 15 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-6
- LVM: fix missing dash in activate_options

  Resolves: rhbz#1612828

* Tue Jul 24 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-4
- gcp-vpc-move-route: new resource agent for Google Cloud

  Resolves: rhbz#1568588

* Fri Jul 20 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-3
- gcp-vpc-move-vip: new resource agent for Google Cloud
- vdo-vol: new resource agent
- LVM-activate: fix issue with dashes
- dont use attribute_target for metadata

  Resolves: rhbz#1568588
  Resolves: rhbz#1538689
  Resolves: rhbz#1513957
  Resolves: rhbz#1602783

* Tue Jul  3 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-2
- VirtualDomain: add stateless support

  Resolves: rhbz#1499894

* Fri Jun 29 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-1
- rebase to v4.1.1
- IPaddr2: add "monitor_retries" parameter

  Resolves: rhbz#1596139
  Resolves: rhbz#1484920

* Mon Jun 25 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-127
- LVM-activate/lvmlockd: new resource agents
- oracle log warning when using sysdba user
- metadata: consistent "s"-suffix for timeout/interval values
- oracle: fix "alter user" syntax
- exportfs: fix IPv6 bracket issue
- SAPHana: improve multiple SR pair supporta (MCOS)
- SAPInstance: add monitored services for ENSA2
- LVM: add "volume_group_check_only" parameter to avoid timeouts

  Resolves: rhbz#1513957
  Resolves: rhbz#1515354
  Resolves: rhbz#1523318
  Resolves: rhbz#1524429
  Resolves: rhbz#1555464
  Resolves: rhbz#1594153
  Resolves: rhbz#1594246
  Resolves: rhbz#1470840

* Thu Feb 22 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-124
- awseip/awsvip: increase default "api_delay" to 3s to avoid failures

  Resolves: rhbz#1500352

* Wed Feb 21 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-123
- awseip: fix for multi-NICs

  Resolves: rhbz#1547218

* Mon Feb 19 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-122
- galera: fix temp logfile rights to support MySQL 10.1.21+

  Resolves: rhbz#1546083

* Mon Feb 12 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-121
- redis: support tunneling replication traffic

  Resolves: rhbz#1543366

* Tue Jan 23 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-120
- sap_redhat_cluster_connector: fix unknown gvi function

  Resolves: rhbz#1536548

* Thu Jan 11 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-119
- NovaEvacuate: add support for keystone v3 authentication

  Resolves: rhbz#1533168

* Mon Dec 11 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-118
- CTDB: detect new config path

  Resolves: rhbz#1523953

* Thu Dec  7 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-117
- ocf_attribute_target: add fallback for Pacemaker versions without
  bundle support

  Resolves: rhbz#1520574

* Fri Dec  1 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-116
- azure-lb: new resource agent
- CTDB: fix initial probe

  Resolves: rhbz#1516435
  Resolves: rhbz#1512580

* Wed Nov 22 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-115
- db2: fix HADR promote when master failed

  Resolves: rhbz#1516180

* Thu Nov  9 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-114
- ethmonitor: add intel omnipath support

  Resolves: rhbz#1364242

* Thu Nov  9 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-113
- galera: recover from empty gvwstate.dat

  Resolves: rhbz#1499677

* Thu Nov  2 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-112
- ethmonitor: VLAN fix
- nfsserver: allow stop to timeout
- portblock: suppress dd output
- LVM: dont use "vgscan --cache"

  Resolves: rhbz#1484473
  Resolves: rhbz#1504112
  Resolves: rhbz#1457382
  Resolves: rhbz#1486888

* Wed Nov  1 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-111
- docker: dont ignore stopped containers
- docker: improve exit reasons

  Resolves: rhbz#bz1508366
  Resolves: rhbz#bz1508362

* Thu Oct 26 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-110
- mysql: fix master score after maintenance mode

  Resolves: rhbz#1465827

* Fri Oct 20 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-109
- awseip/awsvip/aws-vpc-move-ip: new resource agents for Amazon AWS

  Resolves: rhbz#1500352

* Thu Sep 28 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-107
- NovaEvacuate: changes to support Instance HA on OSP12

  Resolves: rhbz#1496393

* Wed Sep 20 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-106
- sybaseASE: new resource agent
- OCF: improve locking
- SAPInstance: add "IS_ERS" parameter for ASCS ERS Netweaver
- VirtualDomain: fix "migrate_options" parsing
- systemd: use tmpfiles.d to create temp directory on boot
- findif: improve IPv6 NIC detection
- support per-host and per-bundle attributes

  Resolves: rhbz#1436189
  Resolves: rhbz#1465822
  Resolves: rhbz#1466187
  Resolves: rhbz#1455305
  Resolves: rhbz#1462802
  Resolves: rhbz#1445628
  Resolves: rhbz#1489734


* Fri Jun 23 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-105
- rabbitmq-cluster: fix to keep expiration policy

  Resolves: rhbz#1342376

* Fri Jun  2 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-104
- SAPHana/SAPHanaTopology: update to version 0.152.21

  Resolves: rhbz#1449681

* Wed May 31 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-102
- LVM: update metadata on start/relocate
- LVM: warn when cache mode is not writethrough

  Resolves: rhbz#1451933

* Tue May 30 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-101
- LVM: status check for missing VG

  Resolves: rhbz#1454699

* Mon May 22 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-100
- docker: add "mount_points" parameter to be able to create directories

  Resolves: rhbz#1452049

* Tue May 16 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-99
- galera: fix bootstrap when cluster has no data

  Resolves: rhbz#1451097

* Wed May  3 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-97
- systemd: add drop-in for clvmd and LVM to avoid fencing on shutdown

  Resolves: rhbz#1316130

* Wed Apr 26 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-96
- IPaddr2: add "preferred_lft" parameter for IPv6

  Resolves: rhbz#1445861

* Fri Apr  7 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-95
- DB2: fix HADR for DB2 V98 or later

  Resolves: rhbz#1427574

* Tue Apr  4 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-94
- send_arp: update usage info

  Resolves: rhbz#1380405

* Tue Apr  4 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-93
- rabbitmq-cluster: allow to run on Pacemaker remote nodes
- oraasm: new resource agent for Oracle ASM

  Resolves: rhbz#1435982
  Resolves: rhbz#1411225

* Tue Mar 28 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-90
- ethmonitor: fix to monitor interface without IP

  Resolves: rhbz#bz1408656

* Tue Mar 28 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-89
- NodeUtilization: new resource agent
- iSCSILogicalUnit, iSCSITarget: make concurrent-safe
- IPaddr2: send gratuitious ARP packets during monitor action
- named: add support for rndc options
- CTDB: fix logging
- IPaddr2: add option to detect duplicate IP

  Resolves: rhbz#1430304
  Resolves: rhbz#1430385
  Resolves: rhbz#1434351
  Resolves: rhbz#1435171
  Resolves: rhbz#1077888
  Resolves: rhbz#1393189

* Thu Mar  9 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-88
- clvm: remove reload action
- iSCSILogicalUnit: add IPv6-support
- IPsrcaddr: fix issue with duplicate routes
- pgsql: don't use crm_failcount
- ocf_log: use same log format as Pacemaker

  Resolves: rhbz#1359252
  Resolves: rhbz#1389300
  Resolves: rhbz#1400172
  Resolves: rhbz#1420565
  Resolves: rhbz#1427611

* Thu Feb  2 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-87
- LVM: fix for "partial vg activates when partial_activation=false"
- redis: notify clients of master being demoted
- SAP/SAP HANA: ppc64le build

  Resolves: rhbz#1392432
  Resolves: rhbz#1305549
  Resolves: rhbz#1371088

* Fri Jan 27 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-86
- SAPDatabase: fix process count for SUSER
- rabbitmq-cluster: reset Mnesia before join

  Resolves: rhbz#1260713
  Resolves: rhbz#1397393

* Fri Jan 13 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-85
- exportfs: fix for IPv6 addresses
- SAPHana/SAPHanaTopology: update to version 0.152.17
- Add netstat dependency

  Resolves: rhbz#1406152
  Resolves: rhbz#1395142
  Resolves: rhbz#1402370

* Tue Dec 20 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-84
- galera: prevent promote after demote
- iSCSITarget: properly create portals for lio-t
- nfsserver: dont stop rpcbind
- Filesystem: submount check
- Delay: change startdelay
- galera: last commit fix for MariaDB 10.1.18+
- portblock: return success on stop with invalid IP
- portblock: use iptables wait

  Resolves: rhbz#1360768
  Resolves: rhbz#1376588
  Resolves: rhbz#1384955
  Resolves: rhbz#1387363
  Resolves: rhbz#1388854
  Resolves: rhbz#1391470
  Resolves: rhbz#1391580
  Resolves: rhbz#1395596

* Tue Nov 29 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-83
- nfsserver: keep options in /etc/sysconfig/nfs
- redis: fix SELinux permissions
- redis: notify clients of master being demoted

  Resolves: rhbz#1387491
  Resolves: rhbz#1390974
  Resolves: rhbz#1305549

* Tue Sep 20 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-82
- portblock: create tickle_dir if it doesn't exist
- tomcat: use systemd if available

  Resolves: rhbz#1303037
  Resolves: rhbz#1249430

* Mon Aug 29 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-81
- oracle: fix issue with C## in monprofile and inform user that
  monuser must start with C## as well for container databases

  Resolves: rhbz#1328386

* Wed Jul 27 2016 Andrew Beekhof <abeekhof@redhat.com> - 3.9.5-80
- rabbit: Allow automatic cluster recovery before forcing it

  Resolves: rhbz#1343905

* Fri Jul 22 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-79
- oracle: use monprofile parameter

  Resolves: rhbz#1358895

* Thu Jul 21 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-78
- nfsserver: fix monitor issues causing NFS to start on
  "debug-monitor" and "resource cleanup"
- nfsserver: remove "up to 10 tries" on start to avoid issues with
  some services taking longer to start
- nfsserver: stop rpc-gssd to allow unmounting of "rpcpipefs_dir"

  Resolves: rhbz#1356866
  Resolves: rhbz#1126073
  Resolves: rhbz#1346733

* Tue Jul  5 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-77
- rabbitmq-cluster: add return codes for not running

  Resolves: rhbz#1342478

* Fri Jun 24 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-76
- rabbitmq-cluster: support dump/restore users for RabbitMQ v. 3.6.x

  Resolves: rhbz#1343905

* Mon Jun  6 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-73
- portblock: fix tickle_tcp bug
- nfsserver: use rpcpipefs_dir variable
- mysql: use replication_port variable
- oracle: inform user that monprofile must start with C## for
  container databases

  Resolves: rhbz#1337109
  Resolves: rhbz#1337615
  Resolves: rhbz#1337124
  Resolves: rhbz#1328386

* Fri Jun  3 2016 Damien Ciabrini <dciabrin@redhat.com> - 3.9.5-72
- garbd: Introduces garbd resource-agent

  Resolves: rhbz#1328018

* Fri May 13 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-71
- nova-compute-wait: fix "Invalid Nova host name" issue

  Resolves: rhbz#1320783

* Tue May  3 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-70
- nfsserver: fix nfs-idmapd fails to start due to
  var-lib-nfs-rpc_pipefs.mount being active

  Resolves: rhbz#1325453

* Tue Apr 26 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-69
- SAP HANA: add Multiple Components One System (MCOS) support
- VirtualDomain: add migration_speed and migration_downtime options
- VirtualDomain: fix unnecessary error when probing nonexistent domain
- oralsnr: fix status check fail when username is more than 8 characters long
- oracle: fix unable to start because of ORA-01081

  Resolves: rhbz#1289107
  Resolves: rhbz#1296406
  Resolves: rhbz#1307160
  Resolves: rhbz#1317578
  Resolves: rhbz#1318985

* Thu Mar 17 2016 Damien Ciabrini <dciabrin@redhat.com> - 3.9.5-68
- galera: recover blocked nodes with --tc-heuristics-recover

  Resolves: rhbz#1284526

* Tue Mar  1 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-67
- sap_redhat_cluster_connector: add support for hostnames with "-"
- NovaEvacuate: simplify nova check
- portblock: new resource agent

  Resolves: rhbz#1265527
  Resolves: rhbz#1287314
  Resolves: rhbz#1303037

* Tue Mar  1 2016 Peter Lemenkov <lemenkov@redhat.com> - 3.9.5-65
- RabbitMQ: keep users during resource reload (small regression fix)

  Resolves: rhbz#1303803

* Tue Mar  1 2016 Peter Lemenkov <lemenkov@redhat.com> - 3.9.5-64
- RabbitMQ: keep users during resource reload

  Resolves: rhbz#1303803

* Tue Mar  1 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-63
- IPaddr2: use IPv6 DAD for collision detection
- nagios: new resource agent

  Resolves: rhbz#1276699
  Resolves: rhbz#1212632

* Mon Feb 29 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-62
- tomcat: fix for SELinux enforced mode
- send_arp: fix buffer overflow on infiniband devices
- mysql: fix tmpfile leak
- VirtualDomain: add migrate_options parameter
- VirtualDomain: fix issue where config file might get removed
- VirtualDomain: fix locale in stop and status functions()

  Resolves: rhbz#1249430
  Resolves: rhbz#1250728
  Resolves: rhbz#1263348
  Resolves: rhbz#1242181
  Resolves: rhbz#1242558
  Resolves: rhbz#1301189

* Mon Feb 22 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-60
- rabbitmq-cluster: fix to forget stopped cluster nodes
- nfsserver: fix systemd status detection

  Resolves: rhbz#1247303
  Resolves: rhbz#1126073

* Wed Feb  3 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-57
- Replace NovaCompute with nova-compute-wait which lets systemd
  manage the nova-compute process

  Resolves: rhbz#1304011

* Wed Feb  3 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-56
- galera: add custom host/port support

  Resolves: rhbz#1299404

* Tue Feb  2 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 3.9.5-55
- NovaCompute/NovaEvacuate: Fix 'evacute' typo
- NovaEvacuate invoke off action

  Resolves: rhbz#1282723
  Resolves: rhbz#1287303

* Mon Sep  7 2015 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.9.5-54
- Fix redis client password regexp
  Resolves: rhbz#1251484

* Thu Sep  3 2015 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.9.5-53
- Add support redis client password authentication
  Resolves: rhbz#1251484

* Thu Jul 23 2015 David Vossel <dvossel@redhat.com> - 3.9.5-52
- Only build SAP hana packages for x86_64

  Resolves: rhbz#1244827

* Thu Jul 23 2015 David Vossel <dvossel@redhat.com> - 3.9.5-51
- Properly include SAP hana packages in correct subpackage.

  Resolves: rhbz#1244827

* Thu Jul 23 2015 David Vossel <dvossel@redhat.com> - 3.9.5-50
- Sync SAP Hana agents with upstream

  Resolves: rhbz#1244827

* Wed Jul 22 2015 David Vossel <dvossel@redhat.com> - 3.9.5-49
- Place SAP Hana agents in sap-hana subpackage

  Resolves: rhbz#1244827

* Fri Jul 10 2015 David Vossel <dvossel@redhat.com> - 3.9.5-48
- add support for oracle resource agents

  Resolves: rhbz#1232376

* Thu Jun 25 2015 David Vossel <dvossel@redhat.com> - 3.9.5-47
- NovaCompute and NovaEvacuate updates
- dhcpd chroot fix
- redis 0byte error fix

  Resolves: rhbz#1214360
  Resolves: rhbz#1227293
  Resolves: rhbz#1231032

* Thu Jun 25 2015 David Vossel <dvossel@redhat.com> - 3.9.5-46
- iface-vlan agent
- Allow partial activation when physical volumes are missing.
- Properly handle 'includes' during apache config parsing
- Support for NovaCompute resource-agent

  Resolves: rhbz#1160365
  Resolves: rhbz#1214781
  Resolves: rhbz#1223615
  Resolves: rhbz#1214360

* Wed Apr 29 2015 David Vossel <dvossel@redhat.com> - 3.9.5-45
- Fix clvmd usage of daemon_options
- Use better default nfsserver start timeouts
- Make nfsserver preserve options in /etc/sysconfig/nfs
- Add link_status_only option to ethmonitor agent
- Add support for nginx agent
- Add support for db2 agent
- CTDB agent updates

  Resolves: rhbz#1171162
  Resolves: rhbz#1173193
  Resolves: rhbz#1182787
  Resolves: rhbz#1213971
  Resolves: rhbz#1183136
  Resolves: rhbz#1059988
  Resolves: rhbz#1077888

* Tue Apr 28 2015 David Vossel <dvossel@redhat.com> - 3.9.5-44
- For IPsrcaddr, properly handle misconfiguration in a way that
  doesn't result in fencing.
- Return exit reason for invalid netmask in IPaddr2

  Resolves: rhbz#1200756
  Resolves: rhbz#773399

* Mon Apr 27 2015 David Vossel <dvossel@redhat.com> - 3.9.5-43
- Add activate_vgs option to clvmd to control activating volume
  groups

  Resolves: rhbz#1198681

* Thu Apr 23 2015 David Vossel <dvossel@redhat.com> - 3.9.5-42
- Improve galera resource-agent to not require use of read-only
  mode to retrieve last known write sequence number.

  Resolves: rhbz#1170376

* Thu Feb 5 2015 David Vossel <dvossel@redhat.com> - 3.9.5-41
- Support for redis resource-agent

  Resolves: rhbz#1189187

* Mon Jan 26 2015 David Vossel <dvossel@redhat.com> - 3.9.5-20.2
- Support for rabbitmq-cluster resource-agent

  Resolves: rhbz#1185754

* Fri Dec 19 2014 David Vossel <dvossel@redhat.com> - 3.9.5-40
- Remove usage of write_back from iSCSILogicalUnit

  Resolves: rhbz#1118029

* Thu Dec 11 2014 David Vossel <dvossel@redhat.com> - 3.9.5-39
- Updates spec file to include iscsi resources

  Resolves: rhbz#1118029

* Mon Oct 27 2014 David Vossel <dvossel@redhat.com> - 3.9.5-38
- Handle invalid monitor_cmd option for docker resource-agent

  Resolves: rhbz#1135026

* Sun Oct 26 2014 David Vossel <dvossel@redhat.com> - 3.9.5-37
- Rename docker agent's 'container' arg to 'name' to avoid confusion
  with pacemaker's metadata 'container' argument.
- Introduce monitor_cmd into docker agent.

  Resolves: rhbz#1135026

* Thu Oct 23 2014 David Vossel <dvossel@redhat.com> - 3.9.5-36
- Fixes cleaning up stale docker containers during stop if
  container instance failed.

  Resolves: rhbz#1135026

* Thu Oct 23 2014 David Vossel <dvossel@redhat.com> - 3.9.5-35
- Introduces docker resource-agent for managing docker containers.
  The docker agent is being released as tech preview.

  Resolves: rhbz#1135026

* Wed Oct 22 2014 David Vossel <dvossel@redhat.com> - 3.9.5-34
- Fixes mysql agents behavior when monitoring resource instance
  when environment validation fails.

  Resolves: rhbz#1138871

* Tue Sep 23 2014 David Vossel <dvossel@redhat.com> - 3.9.5-33
- Merges latest upstream patches for galera agent
- Merges latest upstream patchs for exit reason string

  Resolves: rhbz#1116166
  Resolves: rhbz#1128933

* Wed Sep 17 2014 David Vossel <dvossel@redhat.com> - 3.9.5-32
- Fixes iSCSILogicalUnit syntax error
- Fixes mysql stop operation when db storage is unavailable

  Resolves: rhbz#1118029
  Resolves: rhbz#1138871

* Mon Aug 25 2014 David Vossel <dvossel@redhat.com> - 3.9.5-31
- Man page updates give pcs config examples
- add iscsi agent support
- add infiniband support to ethmonitor
- add resource-agent support of exit reason string
- add safe umount option to Filesystem resource agent

  Resolves: rhbz#1058102
  Resolves: rhbz#1118029
  Resolves: rhbz#1122285
  Resolves: rhbz#1128933
  Resolves: rhbz#1095944

* Fri Aug 15 2014 David Vossel <dvossel@redhat.com> - 3.9.5-30
- Support monitor of lxc without requiring libvirt.
- Wait for filesystem modules to load during start.
- Warn users managing clustered LVM when lvmetad is in use.
- Restore VirtualDomain default start stop timeout values.
- Support exit reason string
- Auto set lvm locking type to clustered when clvmd is in use.

Resolves: rhbz# 1083041
Resolves: rhbz# 1083231
Resolves: rhbz# 1097593
Resolves: rhbz# 1105655
Resolves: rhbz# 1128933
Resolves: rhbz# 773395


* Fri Jul 18 2014 David Vossel <dvossel@redhat.com> - 3.9.5-29
- Support the check_user and check_passwd galera resource-agent
  options.
- Minor NFS agent updates.

  Resolves: rhbz#1116166
  Resolves: rhbz#1091101

* Thu Jul 10 2014 David Vossel <dvossel@redhat.com> - 3.9.5-28
- Updates to nfs server related agent.
- Introduces nfsnotify for sending NFSv3 NSM state change
  notifications allowing NFSv3 clients to reclaim locks.

  Resolves: rhbz#1091101

* Wed Jul 09 2014 David Vossel <dvossel@redhat.com> - 3.9.5-27
- Introducing the galera resource-agent.

  Resolves: rhbz#1116166

* Tue Mar 18 2014 David Vossel <dvossel@redhat.com> - 3.9.5-26
- Handle monitor qemu based VirtualDomain resources without
  requiring libvirtd even if configuration file does not
  contain an 'emulator' value pointing to the emulator binary.

  Resolves: rhbz#1060367

* Fri Feb 14 2014 David Vossel <dvossel@redhat.com> - 3.9.5-25
- Rename clvmd agent to clvm to avoid problems associated
  with having a resource-agent named the same exact name
  as the binary the agent manages.

  Resolves: rhbz#1064512

* Fri Feb 14 2014 David Vossel <dvossel@redhat.com> - 3.9.5-24
- Addition of the clvmd resource-agent
- Support monitoring qemu based VirtualDomain resources without
  requiring libvirtd to be running.

  Resolves: rhbz#1064512
  Resolves: rhbz#1060367

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.9.5-23
- Mass rebuild 2014-01-24

* Mon Jan 20 2014 David Vossel <dvossel@redhat.com> - 3.9.5-22
- Fixes VirtualDomain config parse error.

  Resolves: rhbz#1029061

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.9.5-21
- Mass rebuild 2013-12-27

* Tue Nov 26 2013 David Vossel <dvossel@redhat.com> - 3.9.5-20
- tomcat agent updates for pacemaker support
- slapd agent updates for pacemaker support
- Fixes missing etab file required for nfsserver

  Resolves: rhbz#1033016
  Resolves: rhbz#917681

* Wed Nov 20 2013 David Vossel <dvossel@redhat.com> - 3.9.5-19
- Add back the Delay agent.

  Resolves: rhbz#917681

* Thu Nov 07 2013 David Vossel <dvossel@redhat.com> - 3.9.5-18
- Remove support for (nginx, mysql-proxy, rsyslog). nginx and
  mysql-proxy are not a supported projects. Rsyslog is not an
  agent we will be supporting in an HA environment.

  Resolves: rhbz#917681

* Wed Nov 06 2013 David Vossel <dvossel@redhat.com> - 3.9.5-17
- Split send_ua utility out of IPv6addr.c source so it can be
  re-used in IPaddr2 without requiring cluster-glue.
- Fixes issue with pgsql and SAPInstance not setting transient
  attributes correctly when local corosync node name is not
  equal to 'uname -n'
- High: ocft: Fedora supported test cases

  Resolves: rhbz#917681

* Mon Oct 07 2013 David Vossel <dvossel@redhat.com> - 3.9.5-16
- Fixes issue with mysql agent not being able to set transient
  attributes on local node correctly.
- Fixes bash syntax error in VirtualDomain during 'stop'
- Fixes VirtualDomain default hypervisor usage.
- Fixes VirtualDomain 'start' of pre-defined domain

  Resolves: rhbz#917681
  Resolves: rhbz#1014641
  Resolves: rhbz#1016140

* Thu Sep 26 2013 David Vossel <dvossel@redhat.com> - 3.9.5-15
- Update VirtualDomain heartbeat agent for heartbeat merger.
- Includes upstream fixes for pacemaker_remote lxc test case.

  Resolves: rhbz#917681

* Thu Sep 12 2013 David Vossel <dvossel@redhat.com> - 3.9.5-14
- Add ability for apache agent to perform simple monitoring
  of server request/response without requiring server-status
  to be enabled.
- Fixes invalid return statement in LVM agent.
- Oracle TNS_ADMIN option 

  Resolves: rhbz#917806
  Resolves: rhbz#917681
  Resolves: rhbz#799065

* Mon Sep 9 2013 David Vossel <dvossel@redhat.com> - 3.9.5-13
- Use correct default config for apache
  Resolves: rhbz#1005924

* Tue Jul 30 2013 David Vossel <dvossel@redhat.com> - 3.9.5-12
- Symbolic links do not have file permissions.

* Tue Jul 30 2013 David Vossel <dvossel@redhat.com> - 3.9.5-11
- Fixes file permissions problem detected in rpmdiff test

* Tue Jul 30 2013 David Vossel <dvossel@redhat.com> - 3.9.5-10
- Removes ldirectord package
- Puts sap agents and connector script in subpackage
- exclude unsupported packages
- symlink ipaddr to ipaddr2 so only a single agent is supported

* Mon Jul 29 2013 David Vossel <dvossel@redhat.com> - 3.9.5-9
- Fixes more multi-lib problems.

* Mon Jul 29 2013 David Vossel <dvossel@redhat.com> - 3.9.5-8
- Add runtime dependencies section for Heartbeat agents.
- Fix multi-lib inconsistencies found during rpm diff testing.
- Add dist field back to rpm release name.

* Tue Jul 16 2013 David Vossel <dvossel@redhat.com> - 3.9.5-7
- Detect duplicate resources with the same volgrpname
  name when using exclusive activation with tags

  Resolves: # rhbz984054

* Tue Jun 18 2013 David Vossel <dvossel@redhat.com> - 3.9.5-6
- Restores rsctmp directory to upstream default.

* Tue Jun 18 2013 David Vossel <dvossel@redhat.com> - 3.9.5-5
- Merges redhat provider into heartbeat provider. Remove
  rgmanager's redhat provider.

  Resolves: rhbz#917681
  Resolves: rhbz#928890
  Resolves: rhbz#952716
  Resolves: rhbz#960555

* Tue Mar 12 2013 David Vossel <dvossel@redhat.com> - 3.9.5-4
- Fixes build system error with conditional logic involving
  IPv6addr.

* Mon Mar 11 2013 David Vossel <dvossel@redhat.com> - 3.9.5-3
- Fixes build dependency for pod2man when building against
  rhel-7.

* Mon Mar 11 2013 David Vossel <dvossel@redhat.com> - 3.9.5-2
- Resolves rhbz#915050

* Mon Mar 11 2013 David Vossel <dvossel@redhat.com> - 3.9.5-1
- New upstream release.

* Fri Nov 09 2012 Chris Feist <cfeist@redhat.com> - 3.9.2-5
- Fixed upstream tarball location

* Fri Nov 09 2012 Chris Feist <cfeist@redhat.com> - 3.9.2-4
- Removed version after dist tag
- Resolves: rhbz#875250

* Mon Oct 29 2012 Chris Feist <cfeist@redhat.com> - 3.9.2-3.8
- Remove cluster-glue-libs-devel
- Disable IPv6addr & sfex to fix deps on libplumgpl & libplum (due to
  disappearance of cluster-glue in F18)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.2-3.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul  5 2012 Chris Feist <cfeist@redhat.com> - 3.9.2-3.4
- Fix location of lvm (change from /sbin to /usr/sbin)

* Wed Apr  4 2012 Jon Ciesla <limburgher@gmail.com> - 3.9.2-3.3
- Rebuilt to fix rawhide dependency issues (caused by move of fsck from
  /sbin to /usr/sbin).

* Fri Mar 30 2012 Jon Ciesla <limburgher@gmail.com> - 3.9.2-3.1
- libnet rebuild.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.2-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul  8 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.9.2-2
- add post call to resource-agents to integrate with cluster 3.1.4

* Thu Jun 30 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.9.2-1
- new upstream release
- fix 2 regressions from 3.9.1

* Mon Jun 20 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.9.1-1
- new upstream release
- import spec file from upstream

* Tue Mar  1 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.1-1
- new upstream release 3.1.1 and 1.0.4

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.0-1
- new upstream release
- spec file update:
  Update upstream URL
  Update source URL
  use standard configure macro
  use standard make invokation

* Thu Oct  7 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.17-1
- new upstream release
  Resolves: rhbz#632595, rhbz#633856, rhbz#632385, rhbz#628013
  Resolves: rhbz#621313, rhbz#595383, rhbz#580492, rhbz#605733
  Resolves: rhbz#636243, rhbz#591003, rhbz#637913, rhbz#634718
  Resolves: rhbz#617247, rhbz#617247, rhbz#617234, rhbz#631943
  Resolves: rhbz#639018

* Thu Oct  7 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.16-2
- new upstream release of the Pacemaker agents: 71b1377f907c

* Thu Sep  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.16-1
- new upstream release
  Resolves: rhbz#619096, rhbz#614046, rhbz#620679, rhbz#619680
  Resolves: rhbz#621562, rhbz#621694, rhbz#608887, rhbz#622844
  Resolves: rhbz#623810, rhbz#617306, rhbz#623816, rhbz#624691
  Resolves: rhbz#622576

* Thu Jul 29 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.14-1
- new upstream release
  Resolves: rhbz#553383, rhbz#557563, rhbz#578625, rhbz#591003
  Resolves: rhbz#593721, rhbz#593726, rhbz#595455, rhbz#595547
  Resolves: rhbz#596918, rhbz#601315, rhbz#604298, rhbz#606368
  Resolves: rhbz#606470, rhbz#606480, rhbz#606754, rhbz#606989
  Resolves: rhbz#607321, rhbz#608154, rhbz#608887, rhbz#609181
  Resolves: rhbz#609866, rhbz#609978, rhbz#612097, rhbz#612110
  Resolves: rhbz#612165, rhbz#612941, rhbz#614127, rhbz#614356
  Resolves: rhbz#614421, rhbz#614457, rhbz#614961, rhbz#615202
  Resolves: rhbz#615203, rhbz#615255, rhbz#617163, rhbz#617566
  Resolves: rhbz#618534, rhbz#618703, rhbz#618806, rhbz#618814

* Mon Jun  7 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.13-1
- new upstream release
  Resolves: rhbz#592103, rhbz#593108, rhbz#578617, rhbz#594626
  Resolves: rhbz#594511, rhbz#596046, rhbz#594111, rhbz#597002
  Resolves: rhbz#599643

* Tue May 18 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.12-2
- libnet is not available on RHEL
- Do not package ldirectord on RHEL
  Resolves: rhbz#577264

* Mon May 10 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.12-1
- new upstream release
  Resolves: rhbz#585217, rhbz#586100, rhbz#581533, rhbz#582753
  Resolves: rhbz#582754, rhbz#585083, rhbz#587079, rhbz#588890
  Resolves: rhbz#588925, rhbz#583789, rhbz#589131, rhbz#588010
  Resolves: rhbz#576871, rhbz#576871, rhbz#590000, rhbz#589823

* Mon May 10 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.12-1
- New pacemaker agents upstream release: a7c0f35916bf
  + High: pgsql: properly implement pghost parameter
  + High: RA: mysql: fix syntax error
  + High: SAPInstance RA: do not rely on op target rc when monitoring clones (lf#2371)
  + High: set the HA_RSCTMP directory to /var/run/resource-agents (lf#2378)
  + Medium: IPaddr/IPaddr2: add a description of the assumption in meta-data
  + Medium: IPaddr: return the correct code if interface delete failed
  + Medium: nfsserver: rpc.statd as the notify cmd does not work with -v (thanks to Carl Lewis)
  + Medium: oracle: reduce output from sqlplus to the last line for queries (bnc#567815)
  + Medium: pgsql: implement "config" parameter
  + Medium: RA: iSCSITarget: follow changed IET access policy

* Wed Apr 21 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.11-1
- new upstream release
  Resolves: rhbz#583945, rhbz#581047, rhbz#576330, rhbz#583017
  Resolves: rhbz#583019, rhbz#583948, rhbz#584003, rhbz#582017
  Resolves: rhbz#555901, rhbz#582754, rhbz#582573, rhbz#581533
- Switch to file based Requires.
  Also address several other problems related to missing runtime
  components in different agents.
  With the current Requires: set, we guarantee all basic functionalities
  out of the box for lvm/fs/clusterfs/netfs/networking.
  Resolves: rhbz#570008

* Sat Apr 17 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.10-2
- New pacemaker agents upstream release
  + High: RA: vmware: fix set_environment() invocation (LF 2342)
  + High: RA: vmware: update to version 0.2
  + Medium: Filesystem: prefer /proc/mounts to /etc/mtab for non-bind mounts (lf#2388)
  + Medium: IPaddr2: don't bring the interface down on stop (thanks to Lars Ellenberg)
  + Medium: IPsrcaddr: modify the interface route (lf#2367)
  + Medium: ldirectord: Allow multiple email addresses (LF 2168)
  + Medium: ldirectord: fix setting defaults for configfile and ldirectord (lf#2328)
  + Medium: meta-data: improve timeouts in most resource agents
  + Medium: nfsserver: use default values (lf#2321)
  + Medium: ocf-shellfuncs: don't log but print to stderr if connected to a terminal
  + Medium: ocf-shellfuncs: don't output to stderr if using syslog
  + Medium: oracle/oralsnr: improve exit codes if the environment isn't valid
  + Medium: RA: iSCSILogicalUnit: fix monitor for STGT
  + Medium: RA: make sure that OCF_RESKEY_CRM_meta_interval is always defined (LF 2284)
  + Medium: RA: ManageRAID: require bash
  + Medium: RA: ManageRAID: require bash
  + Medium: RA: VirtualDomain: bail out early if config file can't be read during probe (Novell 593988)
  + Medium: RA: VirtualDomain: fix incorrect use of __OCF_ACTION
  + Medium: RA: VirtualDomain: improve error messages
  + Medium: RA: VirtualDomain: spin on define until we definitely have a domain name
  + Medium: Route: add route table parameter (lf#2335)
  + Medium: sfex: don't use pid file (lf#2363,bnc#585416)
  + Medium: sfex: exit with success on stop if sfex has never been started (bnc#585416)

* Fri Apr  9 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.10-1
- New rgmanager resource agents upstream release
  Resolves: rhbz#519491, rhbz#570525, rhbz#571806, rhbz#574027
  Resolves: rhbz#574215, rhbz#574886, rhbz#576322, rhbz#576335
  Resolves: rhbz#575103, rhbz#577856, rhbz#577874, rhbz#578249
  Resolves: rhbz#578625, rhbz#578626, rhbz#578628, rhbz#578626
  Resolves: rhbz#579621, rhbz#579623, rhbz#579625, rhbz#579626
  Resolves: rhbz#579059

* Wed Mar 24 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.9-2
- Resolves: rhbz#572993 - Patched build process to correctly generate ldirectord man page
- Resolves: rhbz#574732 - Add libnet-devel as a dependancy to ensure IPaddrv6 is built

* Mon Mar  1 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.9-1
- New rgmanager resource agents upstream release
  Resolves: rhbz#455300, rhbz#568446, rhbz#561862, rhbz#536902
  Resolves: rhbz#512171, rhbz#519491

* Mon Feb 22 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.8-1
- New rgmanager resource agents upstream release
  Resolves: rhbz#548133, rhbz#565907, rhbz#545602, rhbz#555901
  Resolves: rhbz#564471, rhbz#515717, rhbz#557128, rhbz#536157
  Resolves: rhbz#455300, rhbz#561416, rhbz#562237, rhbz#537201
  Resolves: rhbz#536962, rhbz#553383, rhbz#556961, rhbz#555363
  Resolves: rhbz#557128, rhbz#455300, rhbz#557167, rhbz#459630
  Resolves: rhbz#532808, rhbz#556603, rhbz#554968, rhbz#555047
  Resolves: rhbz#554968, rhbz#555047
- spec file update:
  * update spec file copyright date
  * use bz2 tarball

* Fri Jan 15 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.7-2
- Add python as BuildRequires

* Mon Jan 11 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.7-1
- New rgmanager resource agents upstream release
  Resolves: rhbz#526286, rhbz#533461

* Mon Jan 11 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.6-2
- Update Pacameker agents to upstream version: c76b4a6eb576
  + High: RA: VirtualDomain: fix forceful stop (LF 2283)
  + High: apache: monitor operation of depth 10 for web applications (LF 2234)
  + Medium: IPaddr2: CLUSTERIP/iptables rule not always inserted on failed monitor (LF 2281)
  + Medium: RA: Route: improve validate (LF 2232)
  + Medium: mark obsolete RAs as deprecated (LF 2244)
  + Medium: mysql: escalate stop to KILL if regular shutdown doesn't work

* Mon Dec 7 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.6-1
- New rgmanager resource agents upstream release
- spec file update:
  * use global instead of define
  * use new Source0 url
  * use %name macro more aggressively

* Mon Dec 7 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.5-2
- Update Pacameker agents to upstream version: bc00c0b065d9
  + High: RA: introduce OCF_FUNCTIONS_DIR, allow it to be overridden (LF2239)
  + High: doc: add man pages for all RAs (LF2237)
  + High: syslog-ng: new RA
  + High: vmware: make meta-data work and several cleanups (LF 2212)
  + Medium: .ocf-shellfuncs: add ocf_is_probe function
  + Medium: Dev: make RAs executable (LF2239)
  + Medium: IPv6addr: ifdef out the ip offset hack for libnet v1.1.4 (LF 2034)
  + Medium: add mercurial repository version information to .ocf-shellfuncs
  + Medium: build: add perl-MailTools runtime dependency to ldirectord package (LF 1469)
  + Medium: iSCSITarget, iSCSILogicalUnit: support LIO
  + Medium: nfsserver: use check_binary properly in validate (LF 2211)
  + Medium: nfsserver: validate should not check if nfs_shared_infodir exists (thanks to eelco@procolix.com) (LF 2219)
  + Medium: oracle/oralsnr: export variables properly
  + Medium: pgsql: remove the previous backup_label if it exists
  + Medium: postfix: fix double stop (thanks to Dinh N. Quoc)
  + RA: LVM: Make monitor operation quiet in logs (bnc#546353)
  + RA: Xen: Remove instance_attribute "allow_migrate" (bnc#539968)
  + ldirectord: OCF agent: overhaul

* Fri Nov 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.5-1
- New rgmanager resource agents upstream release
- Allow pacemaker to use rgmanager resource agents

* Wed Oct 28 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.4-2
- Update Pacameker agents to upstream version: e2338892f59f
  + High: send_arp - turn on unsolicited mode for compatibilty with the libnet version's exit codes
  + High: Trap sigterm for compatibility with the libnet version of send_arp
  + Medium: Bug - lf#2147: IPaddr2: behave if the interface is down
  + Medium: IPv6addr: recognize network masks properly
  + Medium: RA: VirtualDomain: avoid needlessly invoking "virsh define"

* Wed Oct 21 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.4-1
- New rgmanager resource agents upstream release

* Mon Oct 12 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.3-3
- Update Pacameker agents to upstream version: 099c0e5d80db
  + Add the ha_parameter function back into .ocf-shellfuncs.
  + Bug bnc#534803 - Provide a default for MAILCMD
  + Fix use of undefined macro @HA_NOARCHDATAHBDIR@
  + High (LF 2138): IPsrcaddr: replace 0/0 with proper ip prefix (thanks to Michael Ricordeau and Michael Schwartzkopff)
  + Import shellfuncs from heartbeat as badly written RAs use it
  + Medium (LF 2173): nfsserver: exit properly in nfsserver_validate
  + Medium: RA: Filesystem: implement monitor operation
  + Medium: RA: VirtualDomain: loop on status if libvirtd is unreachable
  + Medium: RA: VirtualDomain: loop on status if libvirtd is unreachable (addendum)
  + Medium: RA: iSCSILogicalUnit: use a 16-byte default SCSI ID
  + Medium: RA: iSCSITarget: be more persistent deleting targets on stop
  + Medium: RA: portblock: add per-IP filtering capability
  + Medium: mysql-proxy: log_level and keepalive parameters
  + Medium: oracle: drop spurious output from sqlplus
  + RA: Filesystem: allow configuring smbfs mounts as clones

* Wed Sep 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.3-1
- New rgmanager resource agents upstream release

* Thu Aug 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.1-1
- New rgmanager resource agents upstream release

* Tue Aug 18 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.0-16
- Create an ldirectord package
- Update Pacameker agents to upstream version: 2198dc90bec4
  + Build: Import ldirectord.
  + Ensure HA_VARRUNDIR has a value to substitute
  + High: Add findif tool (mandatory for IPaddr/IPaddr2)
  + High: IPv6addr: new nic and cidr_netmask parameters
  + High: postfix: new resource agent
  + Include license information
  + Low (LF 2159): Squid: make the regexp match more precisely output of netstat
  + Low: configure: Fix package name.
  + Low: ldirectord: add dependency on $remote_fs.
  + Low: ldirectord: add mandatory required header to init script.
  + Medium (LF 2165): IPaddr2: remove all colons from the mac address before passing it to send_arp
  + Medium: VirtualDomain: destroy domain shortly before timeout expiry
  + Medium: shellfuncs: Make the mktemp wrappers work.
  + Remove references to Echo function
  + Remove references to heartbeat shellfuncs.
  + Remove useless path lookups
  + findif: actually include the right header. Simplify configure.
  + ldirectord: Remove superfluous configure artifact.
  + ocf-tester: Fix package reference and path to DTD.

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 3.0.0-15
- Use bzipped upstream hg tarball.

* Wed Jul 29 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-14
- Merge Pacemaker cluster resource agents:
  * Add Source1.
  * Drop noarch. We have real binaries now.
  * Update BuildRequires.
  * Update all relevant prep/build/install/files/description sections.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  8 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-12
- spec file updates:
  * Update copyright header
  * final release.. undefine alphatag

* Thu Jul  2 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-11.rc4
- New upstream release.

* Sat Jun 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-10.rc3
- New upstream release.

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-9.rc2
- New upstream release + git94df30ca63e49afb1e8aeede65df8a3e5bcd0970

* Tue Mar 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-8.rc1
- New upstream release.
- Update BuildRoot usage to preferred versions/names

* Mon Mar  9 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-7.beta1
- New upstream release.

* Fri Mar  6 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-6.alpha7
- New upstream release.

* Tue Mar  3 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-5.alpha6
- New upstream release.

* Tue Feb 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-4.alpha5
- Drop Conflicts with rgmanager.

* Mon Feb 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-3.alpha5
- New upstream release.

* Thu Feb 19 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-2.alpha4
- Add comments on how to build this package.

* Thu Feb  5 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-1.alpha4
- New upstream release.
- Fix datadir/cluster directory ownership.

* Tue Jan 27 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-1.alpha3
  - Initial packaging
