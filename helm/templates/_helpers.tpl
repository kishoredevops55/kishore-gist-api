{{/*
Expand the name of the chart.
*/}}
{{- define "github-gists-api.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "github-gists-api.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "github-gists-api.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "github-gists-api.labels" -}}
helm.sh/chart: {{ include "github-gists-api.chart" . }}
{{ include "github-gists-api.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels - matches existing k8s manifest label: app: github-gists-api
*/}}
{{- define "github-gists-api.selectorLabels" -}}
app: {{ include "github-gists-api.fullname" . }}
app.kubernetes.io/name: {{ include "github-gists-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "github-gists-api.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "github-gists-api.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Namespace helper
*/}}
{{- define "github-gists-api.namespace" -}}
{{- default .Release.Namespace .Values.namespace }}
{{- end }}

{{/*
Service FQDN helper
*/}}
{{- define "github-gists-api.serviceFQDN" -}}
{{- $name := include "github-gists-api.fullname" . -}}
{{- $namespace := include "github-gists-api.namespace" . -}}
{{- printf "%s.%s.svc.cluster.local" $name $namespace }}
{{- end }}
