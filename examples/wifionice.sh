#!/bin/bash

interface="$1"
status="$2"

# essid when script should be called
ESSID="WIFIonICE"

# interface for which script should be called
INTERFACE="${interface}"

# woice python script
WOICE="$(which woice)"


if [ "${interface}" = "${INTERFACE}" ]; then
    # get current essid
    essid="$(iwgetid "${INTERFACE}" -r)"

    # get wifionice status
    wifionicestatus="$("${WOICE}" status)"

    if [ "${essid}" == "${ESSID}" ]; then
        case "${status}" in
            up)
                if [ "${wifionicestatus}" == "down" ]; then
                    logger "Login to WIFI on ICE"
                    "${WOICE}" up
                fi
                ;;
            down)
                if [ "${wifionicestatus}" == "up" ]; then
                    logger "Logout from WIFI on ICE"
                    "${WOICE}" down
                fi
                ;;
        esac
    fi
fi

