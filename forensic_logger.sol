// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ForensicLogger {
    struct IncidentRecord {
        uint256 recordId;
        string incidentHash;
        string sourceIP;
        string destinationIP;
        string attackType;
        uint256 confidenceScore;
        uint256 timestamp;
    }

    IncidentRecord[] public records;
    uint256 public totalIncidents;

    event IncidentLogged(
        uint256 indexed recordId,
        string incidentHash,
        string sourceIP,
        string attackType,
        uint256 confidenceScore,
        uint256 timestamp
    );

    function logIncident(
        string memory _incidentHash,
        string memory _sourceIP,
        string memory _destinationIP,
        string memory _attackType,
        uint256 _confidenceScore
    ) public returns (uint256) {
        totalIncidents++;
        records.push(IncidentRecord(
            totalIncidents,
            _incidentHash,
            _sourceIP,
            _destinationIP,
            _attackType,
            _confidenceScore,
            block.timestamp
        ));

        emit IncidentLogged(totalIncidents, _incidentHash, _sourceIP, _attackType, _confidenceScore, block.timestamp);
        return totalIncidents;
    }

    function getIncident(uint256 _id) public view returns (
        uint256 recordId,
        string memory incidentHash,
        string memory sourceIP,
        string memory destinationIP,
        string memory attackType,
        uint256 confidenceScore,
        uint256 timestamp
    ) {
        require(_id > 0 && _id <= totalIncidents, "Invalid Record ID");
        IncidentRecord memory r = records[_id - 1];
        return (r.recordId, r.incidentHash, r.sourceIP, r.destinationIP, r.attackType, r.confidenceScore, r.timestamp);
    }
}