//dedupe raw into bronze
insert into bronze
select
    json
    ,filename
    ,file_row_nr
    ,file_content_key
    ,file_last_modified
    ,start_scan_time
from raw
qualify row_number() over (
    partition by filename, file_row_nr
    order by file_last_modified desc
) = 1;

//create bronze_view to store as intermediate without unnesting further
create or replace view silver_stage AS
SELECT
    json:"$insert_id"::VARCHAR               AS insert_id,
    //json:"$insert_key"::VARCHAR              AS insert_key,
    //json:"$schema"::VARCHAR                  AS schema_version,
    //json:adid::VARCHAR                       AS adid,
    //json:amplitude_attribution_ids::VARCHAR  AS amplitude_attribution_ids,
    //json:amplitude_event_type::VARCHAR       AS amplitude_event_type,
    json:uuid::VARCHAR                       AS uuid,
    json:amplitude_id::BIGINT                AS amplitude_id,
    json:app::INT                            AS app,
    json:city::VARCHAR                       AS city,
    json:client_event_time::TIMESTAMP_NTZ    AS client_event_time,
    json:client_upload_time::TIMESTAMP_NTZ   AS client_upload_time,
    json:country::VARCHAR                    AS country,
    json:data::VARIANT                       AS data,
    json:data_type::VARCHAR                  AS data_type,
    json:device_brand::VARCHAR               AS device_brand,
    json:device_carrier::VARCHAR             AS device_carrier,
    json:device_family::VARCHAR              AS device_family,
    json:device_id::VARCHAR                  AS device_id,
    json:device_manufacturer::VARCHAR        AS device_manufacturer,
    json:device_model::VARCHAR               AS device_model,
    json:device_type::VARCHAR                AS device_type,
    json:dma::VARCHAR                        AS dma,
    json:event_id::INT                       AS event_id,
    json:event_properties::VARIANT           AS event_properties,
    json:event_time::TIMESTAMP_NTZ           AS event_time,
    json:event_type::VARCHAR                 AS event_type,
    json:global_user_properties::VARIANT     AS global_user_properties,
    json:group_properties::VARIANT           AS group_properties,
    json:groups::VARIANT                     AS groups,
    json:idfa::VARCHAR                       AS idfa,
    json:ip_address::VARCHAR                 AS ip_address,
    json:is_attribution_event::BOOLEAN       AS is_attribution_event,
    json:language::VARCHAR                   AS language,
    json:library::VARCHAR                    AS library,
    json:location_lat::FLOAT                 AS location_lat,
    json:location_lng::FLOAT                 AS location_lng,
    json:os_name::VARCHAR                    AS os_name,
    json:os_version::VARCHAR                 AS os_version,
    json:partner_id::VARCHAR                 AS partner_id,
    json:paying::BOOLEAN                     AS paying,
    json:plan::VARIANT                       AS plan,
    json:platform::VARCHAR                   AS platform,
    json:processed_time::TIMESTAMP_NTZ       AS processed_time,
    json:region::VARCHAR                     AS region,
    json:sample_rate::FLOAT                  AS sample_rate,
    json:server_received_time::TIMESTAMP_NTZ AS server_received_time,
    json:server_upload_time::TIMESTAMP_NTZ   AS server_upload_time,
    json:session_id::BIGINT                  AS session_id,
    json:source_id::VARCHAR                  AS source_id,
    json:start_version::VARCHAR              AS start_version,
    json:user_creation_time::TIMESTAMP_NTZ   AS user_creation_time,
    json:user_id::VARCHAR                    AS user_id,
    json:user_properties::VARIANT            AS user_properties,
    json:version_name::VARCHAR               AS version_name
FROM bronze;

select * from silver_stage
limit 50;

create or replace view silver_event_properties_stage as
select UUID, event_properties
from silver_stage;

select * from silver_event_properties_stage
limit 50;

create or replace view silver_user_properties_stage as
select session_id, amplitude_id user_id, user_properties
from silver_stage;

create or replace table silver_events as
select 
    filename,
    file_row_nr,
    uuid,
    amplitude_id,
    app,
    city,
    client_event_time,
    client_upload_time,
    country,
    data_type,
    device_brand,
    device_carrier,
    device_family,
    device_id,
    device_manufacturer,
    device_model,
    device_type,
    dma,
    event_id,
    event_time,
    event_type,
    global_user_properties,
    group_properties,
    idfa,
    ip_address,
    is_attribution_event,
    language,
    library,
    location_lat,
    location_lng,
    os_name,
    os_version,
    partner_id,
    paying,
    platform,
    processed_time,
    region,
    sample_rate,
    server_received_time,
    server_upload_time,
    session_id,
    source_id,
    start_version,
    user_creation_time,
    user_id,
    user_properties,
    version_name
from silver_stage;


create or replace table silver_event_properties as
select
    b.uuid,
    f.key::VARCHAR              AS property_key,
    f.value::VARCHAR            AS property_value
from silver_event_properties_stage b,
lateral flatten(input => b.event_properties) f;

create or replace table silver_user_properties as
select
    b.session_id,
    b.amplitude_id,
    b.user_id,
    f.key::VARCHAR              AS property_key,
    f.value::VARCHAR            AS property_value
from silver_user_properties_stage b,
lateral flatten(input => b.user_properties) f;